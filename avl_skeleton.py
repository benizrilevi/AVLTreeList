# username - complete info
# id1      - 206484750
# name1    - Guy Reuveni
# id2      - 206388969
# name2    - Ofek Kasif

"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.size = 0

    """returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child
	"""

    def getLeft(self):
        return self.left

    """returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child
	"""

    def getRight(self):
        return self.right

    """returns the parent

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""

    def getParent(self):
        return self.parent

    """return the value

	@rtype: str
	@returns: the value of self, None if the node is virtual
	"""

    def getValue(self):
        return self.value

    """returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""

    def getHeight(self):
        return self.height

    """returns the size

	@rtype: int
	@returns: the size of self, 0 if the node is virtual
	"""

    def getSize(self):
        return self.size

    """returns the balnce factor

    @pre: self is a real node 
	@rtype: int
	@returns: the balance factor of self
	"""

    def getBf(self):
        return self.left.getHeight() - self.right.getHeight()

    """sets left child

	@type node: AVLNode
	@param node: a node
	"""

    def setLeft(self, node):
        self.left = node

    """sets right child

	@type node: AVLNode
	@param node: a node
	"""

    def setRight(self, node):
        self.right = node

    """ sets right child and also sets right child's parent
        @type child: AVLnode
        @param child: a node
     """

    def completeSetRight(self, child):
        self.setRight(child)
        child.setParent(self)

    """ sets left child and also sets right child's parent
        @type child: AVLnode
        @param child: a node
     """

    def completeSetLeft(self, child):
        self.setLeft(child)
        child.setParent(self)

    """sets parent

	@type node: AVLNode
	@param node: a node
	"""

    def setParent(self, node):
        self.parent = node

    """sets value

	@type value: str
	@param value: data
	"""

    def setValue(self, value):
        self.value = value

    """sets the height of the node

	@type h: int
	@param h: the height
	"""

    def setHeight(self, h):
        self.height = h

    """sets the size of the node

	@type size: int
	@param size: the size
	"""

    def setSize(self, size):  # Guy added this method
        self.size = size

    """updates node height by computing it from childrens' height
        and returns 1 as the number of balancing operations that has been done
     """

    def updateHeight(self):
        self.setHeight(max(self.getRight().getHeight(),
                           self.getLeft().getHeight()) + 1)
        return 1

    "updates node size by computing it from childrens' size"

    def updateSize(self):
        self.setSize(self.getRight().getSize() + self.getLeft.GetSize() + 1)


"""given that self is an AVL criminal with BF = -2 and its right son has BF = -1,
    fixes the Bf of self. furthermore, updating the height and size fields of the nodes involved
	"""


def leftRotation(self):
    B = self
    parent = B.getParent()
    A = B.getRight()
    if parent.getLeft() == B:
        parent.setLeft(A)
    else:
        parent.setRight(A)
    A.setParent(parent)
    B.setRight(A.getLeft())
    A.setLeft(B)
    B.getRight().setParent(B)
    B.setParent(A)

    # fixing height field off A and B, the only nodes whose height was changed
    A.updateHeight()
    B.updateHeight()

    # fixing size field off A and B, the only nodes whose size was changed
    A.updateSize()
    B.updateSize()

    """returns whether self is not a virtual node

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""

    def isRealNode(self):
        if self.height == -1:
            return False
        return True


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):

    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None
        self.first = None
        self.last = None

    """ returns list length by getting its' root's size """

    def getLength(self):
        return self.getRoot().getSize()

    """returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""

    def empty(self):
        if self.root == None:
            return True
        return False

    """retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	"""

    def retrieve(self, i):
        return self.treeSelect(i+1).getValue()

    """inserts val at position i in the list

	@type i: int
	@pre: 0 <= i <= self.length()
	@param i: The intended index in the list to which we insert val
	@type val: str
	@param val: the value we inserts
	@rtype: list
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    def insert(self, i, val):
        newNode = AVLNode(val)
        if i == 0:  # inserting the minimum
            if not self.getFirst().isRealNode():  # inserting the root
                self.setRoot(newNode)
                newNode.completeSetLeft(AVLNode())
                newNode.completeSetRight(AVLNode())

            else:
                self.insertLeaf(self.getFirst, newNode, "left")

        elif i == self.getLength():  # inserting the maximum
            self.insertLeaf(self.getLast(), newNode, "right")

        else:
            curr = self.treeSelect(i+1)
            if not curr.getLeft().isRealNode():
                self.insertLeaf(curr, newNode, "left")
            else:
                self.insertLeaf(self.getPredecessorOf(curr), newNode, "right")

        curr, numOfBalancingOp = self.fixAfterInsertion(newNode)
        if curr != None:
            self.increaseSizeByOneAllTheWayUpFrom(curr.getParent())

        return numOfBalancingOp

    """inserts node as a leaf without making any height or size adjustments.
        the adjustments will be done in main insert function
        
        @type currLeaf: AVLNode
        @param currLeaf: the leaf that we want to insert a new son to 
        @type newLeaf: AVLNode
        @param newLeaf: the node that we want to insert as a new leaf
        @type direction: string
        @param direction: indicates if newLeaf will be the left or right son of currLeaf
        @pre: direction = "left" or direction = "right"
        """

    def insertLeaf(self, currLeaf, newLeaf, direction):
        if direction == "right":  # insert newLeaf as right son of currLeaf
            virtualSon = currLeaf.getRight()
            currLeaf.completeSetRight(newLeaf)
        else:  # insert newLeaf as left son of currLeaf
            virtualSon = currLeaf.getLeft()
            currLeaf.completeSetLeft(newLeaf)

        newLeaf.completeSetRight(virtualSon)
        newLeaf.completeSetLeft(AVLNode())

    """travers from the inserted node to tree's root, while looking for criminal AVL subtree
        for every node checked, it updates it size and height.
        if there is no potential AVL criminal subtrees, it will stop and return
        
        @type node: AVLNode
        @param node: inserted node
        return value: tuple
        returns: tuple which its first object is the last node ir checked
                 and second object is number of rebalancing operations that has been done
    """

    def fixAfterInsertion(self, node):
        numOfBalancingOp += node.updateHeight()
        node.updateSize()
        curr = node.getParent()

        while curr != None:
            curr.updateSize()
            prevHeight = curr.getHeight()
            numOfBalancingOp += curr.updateHeight()
            bf = curr.getBf()

            if abs(bf) < 2:
                if prevHeight == curr.getHeight():
                    return (curr, numOfBalancingOp)
                else:
                    curr = curr.getParent()

            else:
                numOfBalancingOp += self.insertRotate(node)
                return (curr, numOfBalancingOp)

        return (curr, numOfBalancingOp)

    """performs rotation on AVL criminal subtree so that self will be legal AVL tree 
        @type node: AVLNode
        @param node: the root of the AVL criminal subtree
        return: int 
        returns: number of rebalancing operation that has been done
    """

    def insertRotate(self, node):
        if node.getBf() == -2:
            if node.getRight().getBf() == -1:
                node.leftRotate()
                return 1
            else:
                node.rightRotate()
                node.leftRotate()  # I'm not sure this is correct
                return 2

        else:
            if node.getLeft().getBf() == 1:
                node.rightRotate()
                return 1
            else:
                node.leftRotate()
                node.rightRotate()
                return 2

    """deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    # not handling mikrey kastze yet.
    def delete(self, i):
        if i >= self.length():
            return -1

        nodeToBeDeleted = self.treeSelect(i+1)

        if i == 0:  # updating first becaus deleting the first item in the list
            self.first = self.getSuccessorOf(nodeToBeDeleted)

        if i == self.length() - 1:  # updating last because deleting the last item in the list
            self.last = self.getPredecessorOf(nodeToBeDelted)

        if self.length() == 1:  # there is only one item in the list and we are deleting it
            self.root = None
            return 0

        if nodeToBeDeleted.getSize() == 1:  # the node is a leaf
            numOfBalancingOpps = deleteLeaf(nodeTobeDeleted)
            return numOfBalancingOpps

        elif not nodeToBeDeleted.getLeft().isRealNode():  # the node has only right child
            numOfBalancingOpps = deleteNodeWithRightChildOnly(nodeToBeDeleted)
            return numOfBalancingOpps

        elif not nodeToBeDeleted.getRight().isRealNode():  # the node has only left child
            numOfBalancingOpps = deleteNodeWithLeftChildOnly(nodeToBeDeleted)
            return numOfBalancingOpps

        else:  # the node has two children
            successor = self.getSuccessorOf(nodeToBeDeleted)
            if successor.size == 1:
                numOfBalancingOpps = deleteLeaf(successor)
            else:
                numOfBalancingOpps = deleteNodeWithRightChildOnly(successor)

            # putting the successor in nodeToBeDeleted place
            parent = nodeToBeDeleted.getParent()
            leftChild = nodeToBeDeleted.getLeft()
            rightChild = nodeToBeDeleted.getRight()
            if parent != None:  # if nodeToBeDeleted is the root then parent == None
                if parent.getLeft() == nodeToBeDeleted:
                    parent.setLeft(successor)
                else:
                    parent.setRight(successor)
            else:
                self.root = successor
            successor.setParent(parent)
            successor.completeSetLeft(leftChild)
            successor.completeSetRight(rightChild)
            return numOfBalancingOpps

        def deleteLeaf(nodeToBeDeleted):
            parent = nodeToBeDeleted.getParent()
            if parent.getLeft() == nodeToBeDeleted:
                parent.completeSetLeft(nodeToBeDeleted.getLeft())
            else:
                parent.completeSetRight(nodeToBeDeleted.getRight())
            nodeToBeDeleted.setParent(None)
            numOfBalancingOpps = fixTreeAfterDeletion(parent)
            return numOfBalancingOpps

        def deleteNodeWithRightChildOnly(nodeToBeDeleted):
            parent = nodeToBeDeleted.getParent()
            child = nodeToBeDeleted.getRight()
            child.setParent(parent)
            if parent != None:  # if nodeToBeDeleted is the root then parent == None
                if parent.getLeft() == nodeToBeDeleted:
                    parent.setLeft(child)
                else:
                    parent.setRight(child)
            else:  # the nodeToBeDeleted is the root and it has only right child, that means that there are only two nodes in the tree, and now the right child becomes the root.
                self.root = child

            nodeToBeDeleted.setParent(None)
            nodeToBeDeleted.setRight(None)
            numOfBalancingOpps = fixTreeAfterDeletion(parent)
            return numOfBalancingOpps

        def deleteNodeWithLeftChildOnly(nodeToBeDeleted):
            parent = nodeToBeDeleted.getParent()
            child = nodeToBeDeleted.getLeft()
            child.setParent(parent)
            if parent != None:  # if nodeToBeDeleted is the root then parent == None
                if parent.getLeft() == nodeToBeDeleted:
                    parent.setLeft(child)
                else:
                    parent.setRight(child)
            else:  # the nodeToBeDeleted is the root and it has only left child, that means that there are only two nodes in the tree, and now the left child becomes the root.
                self.root = child

            nodeToBeDeleted.setParent(None)
            nodeToBeDeleted.setLeft(None)
            numOfBalancingOpps = fixTreeAfterDeletion(parent)
            return numOfBalancingOpps

        def fixTreeAfterDeletion(node):
            numOfBalancingOpps = 0
            doneWithFixingHeight = False
            while node != None:
                node.setSize(node.getSize() - 1)
                if not doneWithFixingHeight:
                    BF = node.getBf()
                    heightBefore = node.getHeight()
                    heightAfter = 1 + \
                        max(node.getLeft().getHeight(),
                            node.getRight().getHeight())
                    if abs(Bf) < 2 and heightAfter == heightBefore:
                        doneWithFixingHeight = True

                    elif abs(BF) < 2 and heightAfter != heightBefore:
                        node.setHeight(heightAfter)
                        numOfBalancingOpps += 1
                    else:  # abs(BF) = 2
                        if heightAfter != heightBefore:
                            node.setHeight(heightAfter)
                        if BF == 2:
                            BFL = node.getLeft().getBf()
                            if BFL == 1 or BFL == 0:
                                self.rightRotation(node)
                                numOfBalancingOpps += 1
                            elif BFL == - 1:
                                self.leftRotation(node)
                                self.rightRotation(node)
                                numOfBalancingOpps += 2
                        else:  # BF = -2
                            BFR = node.getRight().getBf()
                            if BFR == -1 or BFR == 0:
                                self.leftRotatation(node)
                                numOfBalancingOpps += 1
                            elif BFR == 1:
                                self.rightRotation(node)
                                self.leftRotatation(node)
                                numOfBalancingOpps += 2

                node = node.getParent()

            return numOfBalancingOpps

    """returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""

    def first(self):
        if self.empty():
            return None
        return self.first.getValue()

    """returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""

    def last(self):
        if self.empty():
            return None
        return self.last.getValue()

    """returns an array representing list

	@rtype: list
	@returns: a list of strings representing the data structure
	"""

    def listToArray(self):
        return None

    """returns the size of the list

	@rtype: int
	@returns: the size of the list
	"""

    def length(self):
        if self.empty():
            return 0
        return self.getRoot().getSize()

    """splits the list at the i'th index

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list according to whom we split
	@rtype: list
	@returns: a list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
	right is an AVLTreeList representing the list from index i+1, and val is the value at the i'th index.
	"""

    def split(self, i):
        return None

    """concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""

    def concat(self, lst):
        return None

    """searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
	"""

    def search(self, val):
        return None

    """returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""

    def getRoot(self):
        return self.root

    # service methods

    """returns the i'th smallest node in the tree

    @type i: int
    @pre: 1 <= i <= self.length()
    @param i: a position in the tree
    @rtype: AVLNode
    @returns: the i'th smallest node in the tree
    @complexity: O(logi)
    """

    def treeSelect(self, i):
        if i == 1:
            return self.first
        if i == self.length():
            return self.last

        curr = self.findSmallestSubTreeOfSize(i)
        r = curr.getLeft().getSize() + 1
        while (i != r):
            if i < r:               # the node is in the left tree so we need to loof for the i'th smallest node in the left tree
                curr = curr.getLeft()

            # the node is in the right tree so we need to look for the (i-r)'th smallest node in the right tree
            else:
                curr = curr.getRight()
                i = i - r
            r = curr.getLeft().getSize() + 1
        return curr

    """returns the smallest node in the tree whose subtree of size >= k

    @type k: int
    @pre: 1 <= k <= self.length()
    @rtype: AVLNode
    @returns: the smallest node off size >= k
    @complexity: O(logk)
    """

    def findSmallestSubTreeOfSize(self, k):
        curr = self.first
        while (curr.getSize() < k):
            curr = curr.getParent()
        return curr

    """returns the successor of a given node

    @type node: AVLNode
	@rtype: AVLNode
	@returns: the successor of a given node. if the node is the Maximum returns None
    complexity: O(logn)
	"""

    def getSuccessorOf(self, node):
        if self.last == node:
            return None

        if node.getRight().isRealNode():
            curr = node.getRight()
            while curr.isRealNode():
                curr = curr.getLeft()
            return curr

        curr = node.getParent()
        while curr.isRealNode and curr.getRight() == node:
            node = curr
            curr = curr.getParent()
        return curr

    """returns the predecessor of a given node

    @type node: AVLNode
	@rtype: AVLNode
	@returns: the predecessor of a given node. if the node is the minimum returns None
    complexity: O(logn)
	"""

    def getPredecessorOf(self, node):
        if node == self.getFirst():
            return None
        if node.getLeft().isRealNode():
            curr = node.getLeft()
            while curr.getRight().isRealNode():
                curr = curr.getRight()
            return curr
        else:
            curr = node
            # while current node isn't the right son of his parent
            while(curr != curr.getParent().getRight()):
                curr = curr.getParent
            return curr.getParent()

    """increases by 1 the size of all the node which are in the path from node to the root

         @type node: AVLNode
    """

    def increaseSizeByOneAllTheWayUpFrom(self, node):
        while (node != None):
            node.setSize(node.getSize() + 1)
            node = node.getParent

    """given that the node is an AVL criminal with BF = +2 and its left son has BF = +1,
    fixes the Bf of node. furthermore, updating the height and size fields of the nodes involved
	"""

    def rightRotation(self, node):  # not handling the root problem yet
        B = node
        parent = B.getParent()
        A = B.getLeft()
        if parent != None:  # if B is the root then parent == None
            if parent.getLeft() == B:
                parent.setLeft(A)
            else:
                parent.setRight(A)
        else:
            self.root = A
        A.setParent(parent)
        B.setParent(A)
        B.setLeft(A.getRight())
        A.setRight(B)
        B.getLeft().setParent(B)

        # fixing height field off A and B, the only nodes whose height was changed
        A.updateHeight()
        B.updateHeight()

        # fixing size field off A and B, the only nodes whose size was changed
        A.updateSize()
        B.updateSize()
