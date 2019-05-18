from globals import Master, Vernie, traceback, load_message, load_image, LANE_REQUEST


class LaneMaster(Master):
    def __init__(self):
        super(LaneMaster, self).__init__(LANE_REQUEST)
        self.mq.channel.basic_consume(queue=LANE_REQUEST, on_message_callback=self.receive)
        self.mq.channel.start_consuming()

    def receive(self, ch, method, props, body):
        self.log.info('Received message from ' + method.routing_key)
        try:
            code, message, data = load_message(body)
            if code != 200:
                raise Vernie(300, 'Illegal message')
            image = load_image(data)
        except Vernie:
            raise Vernie(300, 'Illegal message')
        except Exception:
            raise Vernie(301, 'Failed to receive message', traceback.format_exc())


def main():
    master = LaneMaster()


if __name__ == "__main__":
    main()
