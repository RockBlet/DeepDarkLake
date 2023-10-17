package main

import (
	"fmt"
	"net"
	"strconv"
	"strings"
)

func dos(ip string, port int) {
	if ip != "None" {
		fmt.Printf("[DOS](%s:%d) - processing", ip, port)
	} else {
		fmt.Println("[err] DOS is imposible")
	}
}

func getIpPort(str string) (string, int) {

	cmdList := strings.Split(str, " ")

	ip := cmdList[1]

	if len(cmdList) > 2 {
		port := cmdList[2]
		iport, _ := strconv.Atoi(port)

		return ip, iport
	}
	return "None", 0
}
func getSourceParram(cmd string) (string, error) {
	paramsList := strings.Split(cmd, " ")

	return paramsList[0], nil
}

// DDOS cmd -> DDOS 163.217.31.78 8888
func source(cmd string) {
	cmdParam, _ := getSourceParram(cmd)

	fmt.Println(cmd)

	switch cmdParam {
	case "/ddos":
		ip, port := getIpPort(cmd)
		dos(ip, port)

	}
}

func main() {
	conn, _ := net.Dial("tcp", "localhost:6666")
	buffer := make([]byte, 1024)

	for {
		n, err := conn.Read(buffer)
		req := string(buffer[:n])

		if err != nil {
			fmt.Println("[Err] -> Connection error in 57 line")
		}

		source(req)
	}
}
