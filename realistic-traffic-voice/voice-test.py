"""Voice test using the ByteBlower Test Framework API."""
import logging  # Use the Python default logging interface
from datetime import timedelta
from os import getcwd
from os.path import join

from byteblower_test_framework.analysis import (  # Flow analysis
    HttpAnalyser,
    VoiceAnalyser,
)
from byteblower_test_framework.endpoint import (  # Traffic endpoint interfaces
    IPv4Port,
    NattedPort,
)
from byteblower_test_framework.host import Server  # Host interfaces
from byteblower_test_framework.logging import \
    configure_logging  # Helper function
from byteblower_test_framework.report import (  # Reporting
    ByteBlowerHtmlReport,
    ByteBlowerJsonReport,
    ByteBlowerUnitTestReport,
)
from byteblower_test_framework.run import Scenario  # Scenario
from byteblower_test_framework.traffic import (  # Traffic generation
    HTTPFlow,
    VoiceFlow,
)

# ByteBlower Server connection parameters
_SERVER = 'byteblower-tutorial-3100.lab.byteblower.excentis.com.'

# ByteBlower Port parameters
_WAN_INTERFACE = 'trunk-1-5'
_CPE_INTERFACE = 'trunk-1-4'

# ByteBlower Port Layer 3 addressing parameters
# Manual IPv4 configuration:
_WAN_IPv4 = '10.8.128.61'
_WAN_NETMASK = '255.255.255.0'
_WAN_GATEWAY = '10.8.128.1'

_CPE_IPv4 = 'dhcp'

# The generated reports will be stored to the 'reports' subdirectory.
_REPORT_PATH = join(getcwd(), 'reports')


def main() -> None:
    """Run the main test procedure."""
    # 1. Create a new Scenario
    scenario = Scenario()

    # Generate a HTML report
    byteblower_html_report = ByteBlowerHtmlReport(output_dir=_REPORT_PATH)
    scenario.add_report(byteblower_html_report)
    # Generate a JUnit XML report
    byteblower_unittest_report = ByteBlowerUnitTestReport(
        output_dir=_REPORT_PATH)
    scenario.add_report(byteblower_unittest_report)
    # Generate a JSON summary report
    byteblower_summary_report = ByteBlowerJsonReport(output_dir=_REPORT_PATH)
    scenario.add_report(byteblower_summary_report)

    # 2. Connect to the ByteBlower server and create & initialize ports

    # Connect to the ByteBlower Server
    server = Server(_SERVER)
    logging.info('Connected to ByteBlower Server %s', server.info)

    # Simulate a host at the WAN-side of the network
    # Create and initialize a ByteBlowerPort on the given interface
    # at the connected ByteBlowerServer
    wan_port = IPv4Port(server,
                        interface=_WAN_INTERFACE,
                        ipv4=_WAN_IPv4,
                        netmask=_WAN_NETMASK,
                        gateway=_WAN_GATEWAY,
                        name='WAN')
    logging.info('Initialized WAN port %r'
                 ' with IP address %r, network %r', wan_port.name, wan_port.ip,
                 wan_port.network)

    # Simulate a host at the CPE-side of the network
    # Create and initialize a ByteBlowerPort on the given interface
    # at the connected ByteBlowerServer
    cpe_port = NattedPort(server,
                          interface=_CPE_INTERFACE,
                          ipv4=_CPE_IPv4,
                          name='CPE')
    logging.info('Initialized CPE port %r'
                 ' with IP address %r, network %r', cpe_port.name, cpe_port.ip,
                 cpe_port.network)

    # 3. Define the traffic test (traffic pattern flows)

    # Downstream Voice flow

    # Create a Voice Stream (G.711)
    ds_voice_flow = VoiceFlow(wan_port,
                              cpe_port,
                              name='Downstream Voice flow',
                              enable_latency=True)

    # Analyze frame loss and latency over time and calculate MOS
    ds_voice_analyser = VoiceAnalyser()
    ds_voice_flow.add_analyser(ds_voice_analyser)

    # Add the downstream Voice flow to the scenario
    scenario.add_flow(ds_voice_flow)
    logging.info('Created downstream Voice flow %s', ds_voice_flow)

    # Upstream Voice flow

    # Create a Voice Stream (G.711)
    us_voice_flow = VoiceFlow(cpe_port,
                              wan_port,
                              name='Upstream Voice flow',
                              enable_latency=True)

    # Analyze frame loss and latency over time and calculate MOS
    us_voice_analyser = VoiceAnalyser()
    us_voice_flow.add_analyser(us_voice_analyser)

    # Add the upstream Voice flow to the scenario
    scenario.add_flow(us_voice_flow)
    logging.info('Created upstream Voice flow %s', us_voice_flow)

    # 4. Define the background traffic

    # Downstream TCP flow

    # Create a TCP Stream of 10s @ 15MBps
    ds_tcp_flow = HTTPFlow(
        wan_port,
        cpe_port,
        name='Downstream background TCP flow',
        request_duration=timedelta(seconds=10),
    )

    # Analyze average goodput (HTTP data) over time
    ds_tcp_analyser = HttpAnalyser()
    ds_tcp_flow.add_analyser(ds_tcp_analyser)

    # Add the downstream TCP flow to the scenario
    scenario.add_flow(ds_tcp_flow)
    logging.info('Created downstream TCP flow %s', ds_tcp_flow)

    # Upstream TCP flow

    # Create a TCP Stream of 10s @ 15MBps
    us_tcp_flow = HTTPFlow(
        cpe_port,
        wan_port,
        name='Upstream background TCP flow',
        request_duration=timedelta(seconds=10),
    )

    # Analyze average goodput (HTTP data) over time
    us_tcp_analyser = HttpAnalyser()
    us_tcp_flow.add_analyser(us_tcp_analyser)

    # Add the upstream TCP flow to the scenario
    scenario.add_flow(us_tcp_flow)
    logging.info('Created upstream TCP flow %s', us_tcp_flow)

    # 5. Run the traffic test

    # Run the scenario (for 12 seconds)
    # The flows will stop after 10s, leaving some additional time for
    # processing the last (delayed?) incoming packets.
    logging.info('Start scenario')
    scenario.run(maximum_run_time=timedelta(seconds=12))

    # 6. Generate test report

    logging.info('Generating report')
    scenario.report()


if __name__ == '__main__':
    # Initialize the Python logging for output to console
    logging.basicConfig(level=logging.INFO)

    # Configures the Python logging so that low-level details
    # are not shown by default.
    configure_logging()

    main()
