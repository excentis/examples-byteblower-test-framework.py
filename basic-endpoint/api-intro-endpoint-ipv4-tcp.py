"""Introduction to the ByteBlower Test Framework Endpoint API."""
import logging  # Use the Python default logging interface
from datetime import timedelta
from os import getcwd
from os.path import join

from byteblower_test_framework.analysis import HttpAnalyser  # Flow analysis
from byteblower_test_framework.endpoint import (  # Traffic endpoint interfaces
    IPv4Endpoint,
    IPv4Port,
)
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
from byteblower_test_framework.traffic import HTTPFlow  # Traffic generation

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
_REPORT_PATH = join(getcwd(), "reports")


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
    logging.info("Connected to ByteBlower Server %s", server.info)

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
        name="WAN",
    )
    logging.info(
        "Initialized WAN port %r"
        " with IP address %r, network %r",
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

    # Downstream TCP flow

    # Create a TCP Stream of 10s @ 4Mbps
    ds_tcp_flow = HTTPFlow(
        wan_port,
        cpe_endpoint,
        name="Downstream TCP flow",
        request_duration=timedelta(seconds=10),
        maximum_bitrate=4000000,
        receive_window_scaling=7,
    )

    # Analyze average goodput (HTTP data) over time
    ds_tcp_analyser = HttpAnalyser()
    ds_tcp_flow.add_analyser(ds_tcp_analyser)

    # Add the downstream TCP flow to the scenario
    scenario.add_flow(ds_tcp_flow)
    logging.info("Created downstream TCP flow %r", ds_tcp_flow.name)

    # Upstream TCP flow

    # Create a TCP Stream of 50MB @ 4Mbps
    us_tcp_flow = HTTPFlow(
        cpe_endpoint,
        wan_port,
        name="Upstream TCP flow",
        request_size=50000000,
        maximum_bitrate=4000000,
        receive_window_scaling=7,
    )

    # Analyze average goodput (HTTP data) over time
    us_tcp_analyser = HttpAnalyser()
    us_tcp_flow.add_analyser(us_tcp_analyser)

    # Add the upstream TCP flow to the scenario
    scenario.add_flow(us_tcp_flow)
    logging.info("Created upstream TCP flow %r", us_tcp_flow.name)

    # 4. Run the traffic test

    # Run the scenario
    # The scenario will run for at least 10 seconds since
    # we have an HTTPFlow with fixed duration of 10s.
    logging.info("Start scenario")
    scenario.run()

    # 5. Generate test report

    logging.info("Generating report")
    scenario.report()


if __name__ == "__main__":
    # Initialize the Python logging for output to console
    logging.basicConfig(level=logging.INFO)

    # Configures the Python logging so that low-level details
    # are not shown by default.
    configure_logging()

    main()
