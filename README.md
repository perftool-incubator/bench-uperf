# bench-uperf
Helper scripts to aid the execution and post-processing of uperf network performance tool.

## Scripts

Name | Description
-----|------------
uperf-base | Checks if the bench-base library can be sourced from the ${TOOLBOX_HOME}/bash/library/ directory. If the library cannot be sourced, the script prints an error message and exits with an exit status of 1.
uperf-client | Runs a network benchmark using uperf, a network performance tool. The script has several command-line options that can be used to customize the benchmark run, including the number of threads, protocol, packet sizes, and duration.
uperf-get-runtime | Outputs the duration of a benchmark run.
uperf-post-process | Perl script that processes results from the uPerf benchmark tool and outputs a JSON file containing performance metrics. The JSON files adhere to a [Common Data Model (CDM) Schema](https://github.com/perftool-incubator/CommonDataModel).
uperf-server-start | Bash script that runs the uperf network performance benchmarking tool as a server. The script sets up the environment for running the tool and starts the server process with the specified parameters.
uperf-server-stop | Stop a uperf server process. The script redirects standard output and standard error to a file named "uperf-server-stop-stderrout.txt".

## JSON files

Name | Description
-----|------------
multiplex.json | Defines presets and validations for the uperf network benchmarking tool. Presets include a set of arguments with predefined values, while validations provide regular expressions for validating the format of the arguments.
rickshaw.json | Describes the configuration for the rickshaw-benchmark and how it interacts with the uperf benchmark, including which files should be transferred to the client and server, and which scripts to execute for starting and stopping the server and client.
workshow.json | Specifies a workshop environment and requirements, including a source code requirement for the "uperf" tool that is downloaded from GitHub and compiled and installed with some specified commands. The environment has a default user environment which requires the "uperf_src" requirement.
