using NUnit.Framework;
using System;
using System.Security.Cryptography.X509Certificates;

namespace DataStructures.Tests
{
    [TestFixture]
public class MaxHeapTests
{
    [Test]
    public void Add_NewHeap_AddsValue()
    {
        // Arrange
        MaxHeap<int> maxHeap = new MaxHeap<int>(5);
        // Act
        maxHeap.Add(13);
        // Assert
        Assert.IsFalse(maxHeap.IsEmpty);
        Assert.AreEqual(13, maxHeap.Peek());
        Assert.AreEqual(1, maxHeap.Count);
    }

    [Test]
    public void IsFull_FullHeap_ReturnsTrue()
    {
        // Arrange
        MaxHeap<int> maxHeap = new MaxHeap<int>(2);
        // Act
        maxHeap.Add(1);
        maxHeap.Add(2);
        // Assert
        Assert.IsTrue(maxHeap.IsFull);
    }
    [Test]
    public void IsFull_EmptyHeap_ReturnsFalse()
    {
        // Arrange
        MaxHeap<int> maxHeap = new MaxHeap<int>(2);
        // Act
        maxHeap.Add(1);
        // Assert
        Assert.IsFalse(maxHeap.IsFull);
    }

    [Test]
    public void IsEmpty_EmptyHeap_ReturnsTrue()
    {
        // Arrange
        MaxHeap<int> maxHeap = new MaxHeap<int>(5);
        // Act
        bool empty = maxHeap.IsEmpty;
        int count = maxHeap.Count;
        // Assert
        Assert.IsTrue(empty);
        Assert.AreEqual(0, count);
    }    

    public void TestAdd()
    {   
        // Arrange
        Exception? caughtException = null;
        MaxHeap<int> maxHeap = new MaxHeap<int>(2);
        // Act
        maxHeap.Add(1);
        maxHeap.Add(2);
        try
        {
            maxHeap.Add(3);
        }
        catch (Exception e)
        {
            caughtException = e;
        }
        // Assert
        Assert.AreEqual(2, maxHeap.Peek());
        Assert.AreEqual(2, maxHeap.Count);
        if (caughtException != null)
        {
            Assert.AreEqual("HeapFullException", caughtException.GetType().Name);
        }
        else
        {
            Assert.Fail("Expected HeapFullException, got null.");
        }
    }

    [Test]
    public void Heapify_EmptyArray_ThrowsException()
    {
        //Arrange
        int[] arr = { };
        Exception? caughtException = null;

        //Act
        try 
        {
            MaxHeap<int>.Heapify(arr);
        }
        catch (Exception e)
        {
            caughtException = e;
        }

        //Assert
        if (caughtException != null)
        {
            Assert.AreEqual("HeapifyEmptyArrayException", caughtException.GetType().Name);
        }
        else
        {
            Assert.Fail("Expected HeapifyEmptyArrayException, got null.");
        }
    }
    [Test]
    public void Heapify_NonEmptyArray_ReturnsHeap()
    {
        // Arrange
        int[] arr = { 1 };
        // Act
        MaxHeap<int> heap = MaxHeap<int>.Heapify(arr);
        // Assert
        Assert.AreEqual(1, heap.Peek());
        Assert.AreEqual(1, heap.Count);
    }

    [Test]
    public void Heapify_Array_ReturnsHeap()
    {
        // Arrange
        int[] arr = { -1, -2, -3, 4, 5 };
        // Act
        MaxHeap<int> heap = MaxHeap<int>.Heapify(arr);
        // Assert
        Assert.AreEqual(5, heap.Peek());
        Assert.AreEqual(5, heap.Count);
    }

    [Test]
    public void HeapSort_EmptyArray_ThrowsException()
    {
        // Arrange
        int[] emptyArr = { };
        Exception? caughtException = null;
        // Act
        try 
        {
            MaxHeap<int>.HeapSort(emptyArr);
        }
        catch (Exception e)
        {
            caughtException = e;
        }
        //Assert
        if (caughtException != null)
        {
            Assert.AreEqual("HeapifyEmptyArrayException", caughtException.GetType().Name);
        }
        else
        {
            Assert.Fail("Expected HeapifyEmptyArrayException, got null.");
        }
    }

    [Test]
    public void HeapSort_SortedArray_ReturnsSortedArray()
    {
        // Arrange
        int[] sortedArr = { 1, 2, 3, 4, 5 };
        // Act
        sortedArr = MaxHeap<int>.HeapSort(sortedArr);
        // Assert
        Assert.AreEqual(new int[] { 1, 2, 3, 4, 5 }, sortedArr);
    }
    
    [Test]
    public void HeapSort_ReverseOrderArray_ReturnsSortedArray()
    {
        // Arrange
        int[] reverseArr = { 5, 4, 3, 2, 1 };
        // Act
        reverseArr = MaxHeap<int>.HeapSort(reverseArr);
        // Assert
        Assert.AreEqual(new int[] { 1, 2, 3, 4, 5 }, reverseArr);
    }

    [Test]
    public void HeapSort_Array_ReturnsSortedArray()
    {
        // Arrange
        int[] arr = { 12, 23, 43, -91, 62, 23 };
        // Act
        arr = MaxHeap<int>.HeapSort(arr);
        // Assert
        Assert.AreEqual(new int[] { -91, 12, 23, 23, 43, 62 }, arr);
    }
    }
}
