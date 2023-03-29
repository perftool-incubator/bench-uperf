# bench-uperf
Helper scripts to aid the execution and post-processing of uperf.

## Files

Name | Description |
-----|-------------|
**Scripts** | |
uperf-base | Sources a library called "bench-base" located in the ${TOOLBOX_HOME}/bash/library directory and prints an error message if the sourcing fails.
uperf-client | Runs the uperf network performance testing tool with various options, based on command-line arguments provided by the user, and saves the results to files called "uperf-client-stderrout.txt" and "uperf-client-result.txt".
uperf-get-runtime | Accepts a command-line argument for the "duration" parameter, using getopt to parse the argument, and then echoes the value of "duration" to the console.
uperf-post-process | Perl script that processes the output of the uperf network benchmarking tool, extracts performance metrics such as throughput and round-trip time, and logs them to a file in a format suitable for use with the [rickshaw](https://github.com/perftool-incubator/rickshaw) benchmarking tool.
uperf-server-start | Starts a uperf benchmark server with optional parameters for CPU pinning, interface selection, and other networking options, and reports on the server's status and network details.
uperf-server-stop | Stops the uperf server by reading its process ID from the file "uperf-server.pid" and sending it a SIGTERM signal, then checking if it is still running and sending it a SIGKILL signal if necessary. The script also logs output to "uperf-server-stop-stderrout.txt".
**JSON** | |
multiplex.json | Contains presets and validations for the uperf benchmark tool, including descriptions and possible values for various arguments.
rickshaw.json | Configuration file for running the uperf benchmark using the Rickshaw benchmarking framework, specifying the files to be copied to the client and server machines, as well as the commands to start and stop the server and client.
workshop.json | Describes a set of workshop-specific user environments and requirements, including the installation of uperf from source with a specific set of commands.
