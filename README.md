# Lab 02: Debugging networked applications

## Overview
Debugging a program that communicates across a network is more challenging, because there are two (or more) programs that are interacting. Consequently, you often need to employ a more sophisticated debugging strategy than using `print` statements or employing a debugger (e.g., `gdb`). In the previous lab, you learned two tools that are useful for debugging networked applications: `netcat` and `netstat`. In this lab you’ll learn some additional tools (`curl` and `tshark`) and strategies for debugging networked applications.


### Learning objectives
After completing this lab, you should be able to:
* Use `tshark` to capture and inspect network packets
* Use `curl` and `netcat` to send and receive HTTP requests and responses
* Use `netstat` to inspect active socket connections


## Getting started
Clone your git repository on the `tigers` servers.

Your task is to correct the bugs in `client_bot.py`. This example application should issue a few HTTP requests and output the data contained in the responses. You should **briefly** describe the bugs you find, how you found them, and how you fixed them in `client_issues.md`. (The `md` extension corresponds to a Markdown file; if you have never used Markdown before, read this [quick primer on Markdown](https://guides.github.com/features/mastering-markdown/).) 

### Background
[Docker](https://www.docker.com/) is a containerization platform that allows applications to run in isolated environments, similar to using a virtual machine (e.g., [VirtualBox](https://www.virtualbox.org/)). However, containers are more lightweight than virtual machines, because they do not include an entire guest operating system. 

![](https://www.eginnovations.com/blog/wp-content/uploads/2020/12/container-vms.jpg)

As you work on this lab, you may want to refer to the [class notes on HyperText Transfer Protocol (HTTP)](https://docs.google.com/document/d/1V-CiXOOc6Ne4_uUMP65ixlFaIsmwEJusZNpRx-mgYuU/edit?usp=sharing) and Project 1.

## Step 1: Run `curl` with Docker

First, you need to understand the intended behavior of `client_bot.py`. The program should issue HTTP requests for two Uniform Resource Indicators (URIs)—[http://picard.cs.colgate.edu/agent.php](http://picard.cs.colgate.edu/agent.php) and [http://picard.cs.colgate.edu/time.php](http://picard.cs.colgate.edu/time.php)—and output the data contained in the responses. You can request these URIs using `curl` to see what data is returned. 

To isolate your requests from others running on the same server, you’ll run `curl` in a Docker container. Your git repo includes a bash script for this purpose:
```bash
$ ./docker_curl.sh http://picard.cs.colgate.edu/agent.php
```

The script builds a Docker image containing `curl` (and a Python wrapper script) and runs a container based on this image. After the container is running, you should see the output:
```
Press Enter to run curl...
```

After your press Enter, curl will run and display the data contained in the HTTP response:
```
Greetings curl/7.64.0
```

The container will keep running until you press Enter again.

Note that the output for [http://picard.cs.colgate.edu/agent.php](http://picard.cs.colgate.edu/agent.php) will be different when you run with `curl` and `client_bot.py`; `client_bot.py` should output “`Greetings client_bot`”.


**🛑 Make sure you can access both URIs using curl (running in Docker), and you understand what output `client_bot.py` should produce.**

## Step 2: Run `client_bot.py` with Docker
Now, you should run `client_bot.py` in a Docker container. Your git repo includes a bash script for this purpose:
```bash
$ ./docker_client.sh picard.cs.colgate.edu 80
```

After the container is running, you should see the output:
```
Press Enter to run client_bot...
```

After you press Enter, an error will occur (recall that `client_bot.py` contains several bugs), and the container will stop running.

If `client_bot.py` does not terminate (normally or abnormally), you can press `ctrl+c` to kill the program and stop the Docker container.
    
**🛑 Make sure you can run `client_bot.py` (in Docker), and an error occurs.**

## Step 3: Running debugging tools
To help you debug `client_bot.py`, you’ll want to take advantage of several tools (described in detail below).  You can run these tools (or any other command) in your Docker container alongside `client_bot.py` (or `curl`). For example, to list the files in the root directory of the docker container, run:
```bash
$ ./docker_exec.sh ls
```

You need to run this command in a **separate** terminal window (connected to the same tigers server) **after** your container is running but **before** you press Enter to run client_bot or curl.

### netstat
`netstat` (which starts for **_network statistics_**) is a command-line tool for listing active sockets. To see sockets that are connected, run:
```bash
$ ./docker_exec.sh netstat -n
```

To see sockets that are listening, run:
```bash
$ ./docker_exec.sh netstat -nl
```

### TShark
TShark is a command-line tool for capturing and analyzing packets. To see all packets entering/exiting your running Docker container, run:
```bash
$ ./docker_exec.sh tshark
```

To see only packets with a source or destination port of 80 (the standard port for HTTP), you can include a filter in your tshark command:
```bash
$ ./docker_exec.sh tshark port 80
```

For each packet, Tshark will output the following information:
* The packet number
* The time the packet was capture (relative to the first packet)
* The source and destination IP addresses — `149.43.80.12` is the IP address for `picard.cs.colgate.edu`; the IP address of your docker container starts with `172.1`
* The highest layer protocol contained in the packet — e.g., TCP (Transmission Control Protocol) is a transport layer protocol; HTTP (HyperText Transfer Protocol) is an application layer protocol
* The length of the highest layer protocol header
* A summary of the contents of the highest layer protocol header

To see the details of the HTTP header, incude the command line argument `-O http`:
```bash
$ ./docker_exec.sh tshark -O http port 80
```
For each packet (or "frame"), Tshark will ouput the following information:
* The number and size of the packet 
* The source (`Src`) and destination (`Dst`) hardware addresses contained in the link layer (i.e., `Ethernet`) header
* The source (`Src`) and destination (`Dst`) Internet Protocol (IP) addresses contained in the network layer (i.e., `Internet Protol`) header
* The source (`Src Port`) and destination (`Dst Port`) ports and sequence (`Seq`) and acknowledgement (`Ack`) numbers included in the transport layer (i.e., `Transmission Conrol Protocol`) header
* The detailed contents of the application layer (i.e., `HyperText Transfer Protocol`) header (if present)

If an HTTP packet is incomplete or improperly formatted, tshark may not be able to "decode" it. In this case, you’ll want to look at the raw payload of the TCP (Transmission Control Protocol) packets, using the command:
```bash
$ ./docker_exec.sh tshark --disable-protocol http  -T fields -e data.data port 80 | ./decode_hex.py
```
(`decode_hex.py` is a script included in your git repo that converts hex to ascii.)

**🛑 Make sure you can run `curl` and `tshark` (in Docker), and you understand the output tshark produces.**

## Step 4: Fix `client_bot.py`

Use `netstat` and TShark to help you fix `client_bot.py`. Remember, you should **briefly** describe the bugs you find, how you found them, and how you fixed them in `client_issues.md`. You will commit both your corrected `client_bot.py` and your completed `client_issues.md` to your git repo.

If you aren’t quite sure what `client_bot.py` is doing wrong, compare the output from `tshark` when you run `curl` with the output from `tshark` when you run `client_bot.py`. (All of these should be run in Docker, as described above.)

## Submission instructions
When you are done, you should commit and push your changes to GitHub.