using NUnit.Framework;
using System;

namespace DataStructures.Tests
{
    [TestFixture]
    public class BinarySearchTreeTests
    {
        [Test]
        public void IsEmpty_NewTree_ReturnsTrue()
        {
            // Arrange
            var bst = new BinarySearchTree<int>();

            // Act
            var result = bst.IsEmpty;

            // Assert
            Assert.IsTrue(result);
        }

        [Test]
        public void Count_NewTree_ReturnsZero()
        {
            // Arrange
            var bst = new BinarySearchTree<int>();

            // Act
            var result = bst.Count;

            // Assert
            Assert.AreEqual(0, result);
        }

        [Test]
        public void Insert_NewTree_InsertsValue()
        {
            // Arrange
            var bst = new BinarySearchTree<int>();

            // Act
            bst.Insert(5);

            // Assert
            Assert.IsFalse(bst.IsEmpty);
            Assert.AreEqual(1, bst.Count);
            Assert.IsTrue(bst.Contains(5));
        }

        [Test]
        public void Insert_DuplicateValue_ThrowsException()
        {
            // Arrange
            var bst = new BinarySearchTree<int>();
            bst.Insert(5);

            // Act & Assert
            Assert.Throws<Exception>(() => bst.Insert(5));
        }

        [Test]
        public void Remove_ValueInTree_RemovesValue()
        {
            // Arrange
            var bst = new BinarySearchTree<int>();
            bst.Insert(5);
            bst.Insert(3);
            bst.Insert(7);

            // Act
            bst.Remove(3);

            // Assert
            Assert.AreEqual(2, bst.Count);
            Assert.IsFalse(bst.Contains(3));
        }

        [Test]
        public void Remove_ValueNotInTree_ThrowsException()
        {
            // Arrange
            var bst = new BinarySearchTree<int>();
            bst.Insert(5);

            // Act & Assert
            Assert.Throws<Exception>(() => bst.Remove(3));
        }

        [Test]
        public void PreorderTraversal_TraversesTreeInPreorder()
        {
            // Arrange
            var bst = new BinarySearchTree<int>();
            bst.Insert(5);
            bst.Insert(3);
            bst.Insert(7);

            var expected = new int[] { 5, 3, 7 };
            var actual = new int[3];
            var index = 0;

            // Act
            bst.Preorder(x => actual[index++] = x);

            // Assert
            Assert.AreEqual(expected, actual);
        }

        [Test]
        public void PostorderTraversal_TraversesTreeInPostorder()
        {
            // Arrange
            var bst = new BinarySearchTree<int>();
            bst.Insert(5);
            bst.Insert(3);
            bst.Insert(7);

            var expected = new int[] { 3, 7, 5 };
            var actual = new int[3];
            var index = 0;

            // Act
            bst.Postorder(x => actual[index++] = x);

            // Assert
            Assert.AreEqual(expected, actual);
        }

        [Test]
        public void InorderTraversal_TraversesTreeInInorder()
        {
            // Arrange
            var bst = new BinarySearchTree<int>();
            bst.Insert(5);
            bst.Insert(3);
            bst.Insert(7);

            var expected = new int[] { 3, 5, 7 };
            var actual = new int[3];
            var index = 0;

            // Act
            bst.Inorder(x => actual[index++] = x);

            // Assert
            Assert.AreEqual(expected, actual);
        }

        // TODO: Add tests for Iterator and Remove() and Contains()

        [Test]
        public void Iterator_TraversesTreeInOrder()
        {
            // Arrange
            var bst = new BinarySearchTree<int>();
            bst.Insert(5);
            bst.Insert(3);
            bst.Insert(7);

            var expected = new int[] { 3, 5, 7 };
            var actual = new int[3];
            var index = 0;

            // Act
            foreach (var value in bst)
            {
                actual[index++] = value;
            }

            // Assert
            Assert.AreEqual(expected, actual);
        }

        [Test]
        public void Iterator_LINQ_MethodSyntax()
        {
            // Arrange
            var bst = new BinarySearchTree<int>();
            bst.Insert(5);
            bst.Insert(3);
            bst.Insert(7);

            var expected = new int[] { 5, 7 };

            // Act
            var actual = bst.Where(x => x > 3).ToArray();

            // Assert
            Assert.AreEqual(expected, actual);
        }
    }
}