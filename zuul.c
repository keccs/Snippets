/* 
 * Simple program to send an output signal on a COM port when 
 * a serial modem receives a call from a list of authorized numbers.
 *
 * Runs on linux.
 * 
 * Wrote this for a phone call-operated garage door opener.
 */

#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <syslog.h>
#include <sys/ioctl.h>

/* Phone tty */
static int fd = -1;
static FILE *file = NULL;

/* Serial output tty */
static char *serial_output = NULL;

void config_port() {
	/* set blocking read */
	fcntl(fd, F_SETFL, 0);
	
	struct termios options;
	tcgetattr(fd, &options);

	/* set baud */
	cfsetispeed(&options, B9600);
	cfsetospeed(&options, B9600);

	options.c_cflag |= (CLOCAL | CREAD);
	
	/* no parity, 8N1 */
	options.c_cflag &= ~PARENB;
	options.c_cflag &= ~CSTOPB;
	options.c_cflag &= ~CSIZE;
	options.c_cflag |= CS8;

	/* enable software flow control */
	options.c_iflag |= (IXON | IXOFF | IXANY);

	/* canonical input mode, no echo */
	options.c_lflag |= ICANON;
	options.c_lflag &= ~ECHO;
	options.c_lflag &= ~ECHOE;

	tcsetattr(fd, TCSANOW, &options);
}

void open_port(char *dev) {
	fd = open(dev, O_RDWR | O_NOCTTY | O_NDELAY);
	if (fd == -1) {
		syslog(LOG_EMERG, "open_port: Cannot open serial port");
		exit(1);
	}
	config_port();
	file = fdopen(fd, "a+");
}

void send_command(const char *command) {
	printf("<  %s\n", command); 
	write(fd, command, strlen(command));
	write(fd, "\r", 1);
}

void list_current_calls() {
	send_command("AT+CLCC");
}

void trim_newline_from_end(char *str) {
	while (1) {
		int len = strlen(str);
		if (len == 0) {
			break;
		}

		char last_char = str[len - 1];
		if (last_char == '\r' || last_char == '\n') {
			str[len - 1] = 0;
		} else {	
			break;
		}
	}
}

int read_numbers_and_verify(char *number) {
	int verified = 0;
	FILE *numbers_file = fopen("/usr/local/etc/zuul-numbers.txt", "r");
	if (!numbers_file) {
		syslog(LOG_ERR, "verify_caller: error opening /usr/local/etc/zuul-numbers.txt");
	} else {
		char verified_number[100];
		while (fgets(verified_number, 100, numbers_file)) {
			trim_newline_from_end(verified_number);
			if (strlen(verified_number) < 5) {
				// skip empty rows
				continue;
			} else if (strstr(number, verified_number) == number) {
				verified = 1;
				break;
			}
		}
		fclose(numbers_file);
	}
	return verified;
}

int verify_caller(char *clcc) {
	int verified = 0;
	char *number = strstr(clcc, ",\"");
	if (number) {
		// skip over ,"
		number = number + 2;
		verified = read_numbers_and_verify(number);
		syslog(LOG_DEBUG, "verify_caller: incoming call: %s", number);
	}
	return verified;
}

void hang_up() {
	send_command("ATH");
}

void send_serial_signal() {
	int ser;
	if ((ser = open(serial_output, O_RDWR | O_NOCTTY | O_NDELAY)) < 0) {
		syslog(LOG_EMERG, "send_serial_signal: Cannot open serial port");	
	}

	int status;
	ioctl(ser, TIOCMGET, &status);

	status |= TIOCM_DTR;
	ioctl(ser, TIOCMSET, &status);

	usleep(2000 * 1000);

	status &= ~TIOCM_DTR;
	ioctl(ser, TIOCMSET, &status);

	close(ser);
}

void handle_current_call_list(char *clcc_result) {
	int verified = verify_caller(clcc_result);
	if (verified) {
		syslog(LOG_DEBUG, "caller verified OK\n");
		hang_up();
		send_serial_signal();
	} else {
		syslog(LOG_INFO, "caller verify failed");
	}
}

void on_sigint(int sig) {	
	syslog(LOG_INFO, "received SIGINT, exiting");

	FILE *old_file = file;
	file = NULL;
	fclose(old_file);

	int old_fd = fd;
	fd = -1;
	close(old_fd);
}

int main(int argc, char **argv) {
	if (argc != 3) {
		printf("Usage: zuul PHONE_DEV SERIAL_DEV\n");
		exit(1);
	}

	open_port(argv[1]);
	serial_output = argv[2];

	printf("zuul started, messages will be logged to syslog");
	openlog("zuul", LOG_CONS, LOG_DAEMON);	
	
	syslog(LOG_INFO, "started");
	syslog(LOG_INFO, "phone input tty: %s", argv[1]);
	syslog(LOG_INFO, "serial output tty: %s", argv[2]);

	signal(SIGINT, on_sigint);
	while (file != NULL && fd != -1) {
		char buffer[100];
		if (fgets(buffer, 100, file)) {
			syslog(LOG_DEBUG, " > %s", buffer);
			if (strstr(buffer, "RING") == buffer) {
				list_current_calls();
			} else if (strstr(buffer, "+CLCC") == buffer) {
				handle_current_call_list(buffer);
			} else if (strstr(buffer, "ERROR") == buffer) {
				usleep(1000 * 1000);
				list_current_calls();
			}
		}
	}

	closelog();
	
	return 0;
}
