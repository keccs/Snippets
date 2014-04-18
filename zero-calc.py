#
# script to compare electric and gasoline powered bikes fuel prices
#

motorcycle_price_usd = 2000.0 # cost of the bike
motorcycle_litres_per_100km = 2.5
gas_price_per_litre_usd = 2.0

zero_price_usd = 10000.0 # cost of the zero
zero_kwh_per_km = 8.5 / 165.0 # 8.5kwh battery, 165km city riding
electricity_price_per_kwh = 0.25

def motorcycle_price_per_km():
	return motorcycle_litres_per_100km / 100.0 * gas_price_per_litre_usd

def zero_price_per_km():
	return electricity_price_per_kwh * zero_kwh_per_km

print('motorcycle_price_per_km: %5.3f$' % motorcycle_price_per_km())
print('zero_price_per_km: %5.3f$\n' % zero_price_per_km())

for kms in range(0, 300000, 50000):
	motorcycle_fuel_price = motorcycle_price_per_km() * kms
	zero_fuel_price = zero_price_per_km() * kms
	saving = 'SAVING' if motorcycle_fuel_price - zero_fuel_price > zero_price_usd - motorcycle_price_usd else 'LOSS  '
	print('%s after %6dkms    Motorcycle:%6d$ zero:%6d$' % (saving, kms, motorcycle_fuel_price, zero_fuel_price))
