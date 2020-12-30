#!/usr/bin/python3
import grpc

import spacex.api.device.device_pb2
import spacex.api.device.device_pb2_grpc

with grpc.insecure_channel('192.168.100.1:9200') as channel:
    stub = spacex.api.device.device_pb2_grpc.DeviceStub(channel)
    response = stub.Handle(spacex.api.device.device_pb2.Request(get_status={}))

status = response.dish_get_status

# More alerts may be added in future, so rather than list them individually,
# build a bit field based on field numbers of the DishAlerts message.
alert_bits = 0
for alert in status.alerts.ListFields():
    alert_bits |= (1 if alert[1] else 0) << (alert[0].number - 1)

print(",".join([status.device_info.id, status.device_info.hardware_version, status.device_info.software_version,
    spacex.api.device.dish_pb2.DishState.Name(status.state)]) + "," +
    ",".join(str(x) for x in [status.device_state.uptime_s, status.snr, status.seconds_to_first_nonempty_slot,
    status.pop_ping_drop_rate, status.downlink_throughput_bps, status.uplink_throughput_bps,
    status.pop_ping_latency_ms, alert_bits, status.obstruction_stats.fraction_obstructed,
    status.obstruction_stats.currently_obstructed, status.obstruction_stats.last_24h_obstructed_s]) + "," +
    ",".join(str(x) for x in status.obstruction_stats.wedge_abs_fraction_obstructed))