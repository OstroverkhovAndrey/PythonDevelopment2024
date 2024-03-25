
import asyncio
import cowsay

clients = {} # ip -> queue
ip_to_cow = {} # ip -> cow_name
cow_to_ip = {} # cow_name -> ip

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                comand = q.result().decode().strip().split()
                print(comand)

                request_num = None
                if len(comand) > 0 and comand[0].isnumeric():
                    request_num = comand[0]
                    comand = comand[1:]

                match comand:
                    case ["who"]:
                        who = " ".join(list(cow_to_ip.keys()))
                        if request_num != None:
                            who = str(request_num) + " " + who
                        writer.write(who.encode())
                        await writer.drain()
                    case ["cows"]:
                        cows = []
                        for cow in cowsay.list_cows():
                            if cow not in cow_to_ip:
                                cows.append(cow)
                        cows = " ".join(cows)
                        if request_num:
                            cows = str(request_num) + " " + cows
                        writer.write(cows.encode())
                        await writer.drain()
                    case ["login", cow_name]:
                        if me in ip_to_cow:
                            ans = "Вы уже залогинены"
                        elif cow_name in cowsay.list_cows() and cow_name not in cow_to_ip:
                            cow_to_ip[cow_name] = me
                            ip_to_cow[me] = cow_name
                            ans = "Вы успешно залогинились, логин {}".format(cow_name)
                        else:
                            ans = "Некоректное имя коровы"
                        if request_num:
                            ans = str(request_num) + " " + ans
                        writer.write(ans.encode())
                        await writer.drain()

                    case ["say", cow_name, *msg]:
                        if me in ip_to_cow:
                            if cow_name in cow_to_ip:
                                msg = q.result().decode()[len(request_num):].strip()
                                msg = msg[3:].strip()
                                msg = msg[len(cow_name):].strip()
                                msg = cowsay.cowsay(message=msg, cow=ip_to_cow[me])
                                out = clients[cow_to_ip[cow_name]]
                                await out.put("{} {}:\n{}".format(request_num, ip_to_cow[me], msg))
                            else:
                                ans = "Нет такого пользователя"
                                if request_num:
                                    ans = str(request_num) + " " + ans
                                writer.write(ans.encode())
                                await writer.drain()
                        else:
                            ans = "Вы не залогинены, чтобы отправлять сообщения залогиньтесь"
                            if request_num:
                                ans = str(request_num) + " " + ans
                            writer.write(ans.encode())
                            await writer.drain()

                    case ["yield", *msg]:
                        if me in ip_to_cow:
                            msg = q.result().decode()[len(request_num):].strip()
                            msg = msg[5:].strip()
                            msg = cowsay.cowsay(message=msg, cow=ip_to_cow[me])
                            for ip, out in clients.items():
                                if out is not clients[me] and ip in ip_to_cow:
                                    await out.put("{} {}:\n{}".format(request_num, ip_to_cow[me], msg))
                        else:
                            ans = "Вы не залогинены, чтобы отправлять сообщения залогиньтесь"
                            if request_num:
                                ans = str(request_num) + " " + ans
                            writer.write(ans.encode())
                            await writer.drain()

                    case ["quit"]:
                        if me in ip_to_cow:
                            ans = "Вы разлогинились, логин {}".format(ip_to_cow[me])
                            del cow_to_ip[ip_to_cow[me]]
                            del ip_to_cow[me]
                            if request_num:
                                ans = str(request_num) + " " + ans
                            writer.write(ans.encode())
                            await writer.drain()
                        else:
                            ans = "Вы не были залогинены"
                            if request_num:
                                ans = str(request_num) + " " + ans
                            writer.write(ans.encode())
                            await writer.drain()


                send = asyncio.create_task(reader.readline())

            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del cow_to_ip[ip_to_cow[me]]
    del ip_to_cow[me]
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())

