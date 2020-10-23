# 物联网感知技术课设

[![github](https://img.shields.io/badge/python-tkinter-brightgreen.svg)](https://github.com/snowdreams1006)[![github](https://img.shields.io/badge/OS-MacOS-blue.svg)](https://github.com/snowdreams1006)

## Project 1 五子棋

### 在线对战

#### 服务器

最多建立16个用户连接。对于每个用户，采用双线程设计，一个线程负责发送数据，另一个线程负责接收数据。

> 发送线程
>
> 当两个用户端没有建立起对战连接时，向客户端不断发送实时用户列表和他们各自的准备状态。

> 接收线程
>
> 接收类型：
>
> 1. answer：用于客户端应答请求，分为接收和拒绝。服务器要将应答结果发送给请求客户端。如果应答为接收，那么服务器将建立对战连接。
> 2. request：服务器接收请求和请求对象，并对请求对象发送求情和请求端信息。
> 3. position：对战连接，发送接收棋子位置，并转发。

#### 客户端

接收客户端的信息，并作出相应的处理。