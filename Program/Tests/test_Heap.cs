using NUnit.Framework;
using System;

namespace DataStructures.Tests
{
    [TestFixture]
public class MaxHeapTests
{
    [Test]
    public void TestHeapSort()
    {
        int[] arr = { 12, 11, 13, 5, 6, 7 };
        MaxHeap<int>.HeapSort(arr);
        Assert.AreEqual(new int[] { 5, 6, 7, 11, 12, 13 }, arr);
    }

    // [Test]
    // public void TestHeapify()
    // {
        // int[] arr = { 12, 11, 13, 5, 6, 7 };
        // MaxHeap<int>.Heapify(arr);
    // }
}
}