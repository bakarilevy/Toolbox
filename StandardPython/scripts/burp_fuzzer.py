import random

from java.util import List, ArrayList

from burp import IBurpExtender
from burp import IIntruderPayloadGenerator
from burp import IIntruderPayloadGeneratorFactory


class CustomFuzzer(IIntruderPayloadGenerator):
    
    def __init__(self, extender, attack):
        self._extender = extender
        self._helper = extender._helpers
        self._attack = attack
        self.max_payloads = 10
        self.num_iterations = 0
        return

    def hasMorePayloads(self):
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True
    
    def getNextPayload(self, current_payload):
        # Convert into a string
        payload = "".join(chr(x) for x in current_payload)
        # Call a simple mutator to fuzz the POST
        payload = self.mutatePayload(payload)
        # Increase the number of fuzzing attempts
        self.num_iterations += 1
        return payload

    def mutatePayload(self, original_payload):
        # Pick a simple mutator or call an external script
        picker = random.randint(1,3)
        # Select a random offset in the payload to mutate
        offset = random.randint(0, len(original_payload) - 1)
        front, back = original_payload[:offset], original_payload[offset:]
        # Random offset insert a SQL injection attempt
        if picker == 1:
            front += "'"
        # Try an XSS attempt
        elif picker == 2:
            front += "<script>alert('Burpsuite XSS!');</script>"
        # Repeat a random chunk of the original payload
        elif picker == 3:
            chunk_length = random.randint(0, len(back) - 1)
            repeater = random.randint(1, 10)
            for _ in range(repeater):
                front += original_payload[:offset + chunk_length]
        return front + back
    
    def reset(self):
        self.num_iterations = 0
        return


class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        
        callbacks.registerIntruderPayloadGeneratorFactory(self)
        
        return

    def getGeneratorName(self):
        return "Custom Python Payload Generator"

    def createNewInstance(self, attack):
        return CustomFuzzer(self, attack)