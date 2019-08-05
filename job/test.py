

class Test:

    @staticmethod
    def run(channel, method_frame, header_frame, body):
        print(
            channel,
            method_frame,
            header_frame,
            body
        )