# Timezone and DST

The legacy time engine remains responsible for broker-to-UTC and UTC-to-New-York conversion during the pilot. The adapter records canonical observation timestamps in UTC milliseconds. Differential fixtures must include DST boundary days before promotion beyond pilot status.
