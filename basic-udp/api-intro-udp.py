"""Introduction to the ByteBlower Test Framework API."""
import logging  # Use the Python default logging interface
from datetime import timedelta
from os import getcwd
from os.path import join

from byteblower_test_framework.analysis import (  # Flow analysis
    LatencyFrameLossAnalyser,
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
    FrameBlastingFlow,
    IPv4Frame,
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

    # 3. Define the traffic test (flows)

    # Downstream UDP flow (frame blasting)

    # Create a UDP frame
    # Enable the "latency tagging" so we can analyze latency
    ds_frame = IPv4Frame(latency_tag=True)
    # Create a Stream of 10s @ 1000fps
    ds_udp_flow = FrameBlastingFlow(wan_port,
                                    cpe_port,
                                    name='Downstream UDP flow',
                                    frame_rate=1000,
                                    number_of_frames=10000,
                                    frame_list=[ds_frame])

    # Analyze frame loss and latency over time
    ds_udp_analyser = LatencyFrameLossAnalyser()
    ds_udp_flow.add_analyser(ds_udp_analyser)

    # Add the downstream UDP flow to the scenario
    scenario.add_flow(ds_udp_flow)
    logging.info('Created downstream UDP flow %s', ds_udp_flow)

    # Upstream UDP flow (frame blasting)

    # Create a UDP frame
    # Enable the "latency tagging" so we can analyze latency
    us_frame = IPv4Frame(latency_tag=True)
    # Create a Stream of 10s @ 500fps
    us_udp_flow = FrameBlastingFlow(cpe_port,
                                    wan_port,
                                    name='Upstream UDP flow',
                                    frame_rate=500,
                                    number_of_frames=5000,
                                    frame_list=[us_frame])

    # Analyze frame loss and latency over time
    us_udp_analyser = LatencyFrameLossAnalyser()
    us_udp_flow.add_analyser(us_udp_analyser)

    # Add the upstream UDP flow to the scenario
    scenario.add_flow(us_udp_flow)
    logging.info('Created upstream UDP flow %s', us_udp_flow)

    # 4. Run the traffic test

    # Run the scenario
    # The scenario will run for 10 seconds since we have a limited
    # number of frames configured in the FrameBlastingFlows.
    logging.info('Start scenario')
    scenario.run()

    # 5. Generate test report

    logging.info('Generating report')
    scenario.report()


if __name__ == '__main__':
    # Initialize the Python logging for output to console
    logging.basicConfig(level=logging.INFO)

    # Configures the Python logging so that low-level details
    # are not shown by default.
    configure_logging()

    main()
