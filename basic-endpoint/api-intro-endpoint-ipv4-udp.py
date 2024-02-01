"""Introduction to the ByteBlower Test Framework API Endpoint."""
import logging  # Use the Python default logging interface
from os import getcwd
from os.path import join

from byteblower_test_framework.analysis import \
    LatencyFrameLossAnalyser  # Flow analysis
from byteblower_test_framework.endpoint import (  # Traffic endpoint interfaces
    IPv4Endpoint,
    IPv4Port,
)
from byteblower_test_framework.factory import create_frame
from byteblower_test_framework.host import MeetingPoint  # Host interfaces
from byteblower_test_framework.host import Server
from byteblower_test_framework.logging import \
    configure_logging  # Helper function
from byteblower_test_framework.report import (  # Reporting
    ByteBlowerHtmlReport,
    ByteBlowerJsonReport,
    ByteBlowerUnitTestReport,
)
from byteblower_test_framework.run import Scenario  # Scenario
from byteblower_test_framework.traffic import \
    FrameBlastingFlow  # Traffic generation

# ByteBlower Server connection parameters
_SERVER = 'byteblower-integration-3100-1.lab.byteblower.excentis.com.'

# ByteBlower Meeting Point connection parameters
_MEETING_POINT = 'byteblower-integration-3100-1.lab.byteblower.excentis.com.'

# ByteBlower Port parameters
_WAN_INTERFACE = "trunk-1-23"

# DHCP IPv4 Configuration
_WAN_IPv4 = "dhcp"

# ByteBlower Port parameters
# Unique Identifier (UUID) of the ByteBlower Endpoint application
_UUID: str = '017d7da0-9724-4459-a037-bcec9acf577a'

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
        output_dir=_REPORT_PATH
    )
    scenario.add_report(byteblower_unittest_report)
    # Generate a JSON report
    byteblower_json_report = ByteBlowerJsonReport(output_dir=_REPORT_PATH)
    scenario.add_report(byteblower_json_report)

    # 2. Connect to the ByteBlower hosts and create & initialize endpoints

    # Connect to the ByteBlower Server
    server = Server(_SERVER)
    logging.info('Connected to ByteBlower Server %s', server.info)

    # Connect to the ByteBlower Meeting Point
    meeting_point = MeetingPoint(_MEETING_POINT)
    logging.info(
        "Connected to ByteBlower meeting point %s",
        meeting_point.info,
    )

    # Simulate a host at the WAN-side of the network
    # Create and initialize a ByteBlowerPort on the given interface
    # at the connected ByteBlowerServer
    wan_port = IPv4Port(
        server,
        interface=_WAN_INTERFACE,
        ipv4=_WAN_IPv4,
        name='WAN',
    )
    logging.info(
        'Initialized WAN port %r'
        ' with IP address %r, network %r',
        wan_port.name,
        wan_port.ip,
        wan_port.network,
    )

    # Simulate a host at the CPE-side of the network
    # Create and initialize a ByteBlowerEndpoint on the given device
    # at the connected Meeting Point
    cpe_endpoint = IPv4Endpoint(meeting_point, _UUID)
    logging.info(
        "Initialized CPE endpoint %r"
        " with UUID %r",
        cpe_endpoint.name,
        cpe_endpoint.uuid,
    )

    # 3. Define the traffic test (flows)

    # Downstream UDP flow (frame blasting)

    # Create a UDP frame
    # Enable the "latency tagging" so we can analyze latency
    ds_frame = create_frame(wan_port, latency_tag=True)
    # Create a Stream of 10s @ 1000fps
    ds_udp_flow = FrameBlastingFlow(
        wan_port,
        cpe_endpoint,
        name='Downstream UDP flow',
        frame_rate=1000,
        number_of_frames=10000,
        frame_list=[ds_frame],
    )

    # Analyze frame loss and latency over time
    ds_udp_analyser = LatencyFrameLossAnalyser()
    ds_udp_flow.add_analyser(ds_udp_analyser)

    # Add the downstream UDP flow to the scenario
    scenario.add_flow(ds_udp_flow)
    logging.info('Created downstream UDP flow %r', ds_udp_flow.name)

    # Upstream UDP flow (frame blasting)

    # Create a UDP frame
    # Enable the "latency tagging" so we can analyze latency
    us_frame = create_frame(cpe_endpoint, latency_tag=True)
    # Create a Stream of 10s @ 500fps
    us_udp_flow = FrameBlastingFlow(
        cpe_endpoint,
        wan_port,
        name='Upstream UDP flow',
        frame_rate=500,
        number_of_frames=5000,
        frame_list=[us_frame],
    )

    # Analyze frame loss and latency over time
    us_udp_analyser = LatencyFrameLossAnalyser()
    us_udp_flow.add_analyser(us_udp_analyser)

    # Add the upstream UDP flow to the scenario
    scenario.add_flow(us_udp_flow)
    logging.info('Created upstream UDP flow %r', us_udp_flow.name)

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
