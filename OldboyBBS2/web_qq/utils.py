import models
import Queue

class ChatHandle(object):
    def __init__(self):
        self.queue = Queue.Queue()


    def get_msg(self,request):
        new_msgs = []
        if self.queue.qsize() >0:#has new msg
            for i in range(self.queue.qsize()):
                msg = self.queue.get_nowait()
                new_msgs.append(msg)

        else:#has no new msg
            print '\033[41;1mNo new msg for user [%s] waiting for 60 secs\033[0m' %(request.user.userprofile.name)
            try:
                new_msgs.append(self.queue.get(timeout=60))

            except Queue.Empty,e:
                print '\033[41;1mTimeout of waiting for new msgs for user [%s]\033[0m' %(request.user.userprofile.name)
                return  new_msgs
        print "\033[33;1mFound new [%s]msgs as below\033[0m" % len(new_msgs),new_msgs
        return new_msgs
    def get_contacts(self):
        pass

