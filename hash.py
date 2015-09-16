import md5

class Hash(object):
    def __init__(self, nodes=None):
        """Manages a hash ring.

        `nodes` is a list of objects that have a proper __str__ representation.
        `replicas` indicates how many virtual points should be used pr. node,
        replicas are required to improve the distribution.
        """

        self.ring = dict()
        self._sorted_keys = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        """
        Adds a `node` to the hash ring (including a number of replicas).
        """
        key = self.gen_key(node)
        self.ring[node] = key
        

    def remove_node(self, node):
        """Removes `node` from the hash ring and its replicas.
        """
        #key = self.gen_key('%s:%s' % (node, i))
        del self.ring[node]
        #self._sorted_keys.remove(key)

    def get_node(self, string_key):
        if not self.ring:
            return None

        key = self.gen_key(string_key)

        #nodes = self._sorted_keys
        minimum = self.ring[self.ring.keys()[0]] - key;
        min_node = self.ring.keys()[0];

        for i in self.ring.keys():
            if self.ring[i]-key < minimum:        
                minimum = self.ring[i]-key;
                min_node = i;
                
        return min_node;

    def gen_key(self, key):
        """Given a string key it returns a long value,
        this long value represents a place on the hash ring.

        md5 is currently used because it mixes well.
        """
        m = md5.new()
        m.update(key)
        return int(m.hexdigest(), 16)