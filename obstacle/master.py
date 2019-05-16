import cv2
import numpy as np

from globals import Master, load_message, OBST_REQUEST


class ObstMaster(Master):
    def __init__(self):
        super(ObstMaster, self).__init__(OBST_REQUEST)
        self.mq.channel.basic_consume(queue=OBST_REQUEST, on_message_callback=self.receive)
        self.mq.channel.start_consuming()

    def receive(self, ch, method, props, body):
        self.log.info('************ Received Request ************')
        try:
            code, message, image_dict = load_message(body)
            if code != 200:
                raise Exception
            windshield = cv2.imdecode(np.fromstring(image_dict['windshield'], np.uint8), 1)
        except Exception:
            pass


def main():
    master = Master()


if __name__ == "__main__":
    main()
