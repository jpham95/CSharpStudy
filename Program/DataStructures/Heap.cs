#nullable enable

using System;
using System.Collections.Generic;
using Microsoft.VisualStudio.TestPlatform.CommunicationUtilities;
using NUnit.Framework.Constraints;

namespace DataStructures
{
    public class MaxHeap<T> where T : IComparable<T>
    {
        // Variables
        private int MinCapacity = 1;
        private int length;
        private T[] array;
        // Constructor
        public MaxHeap(int maxSize)
        {
            this.length = 0;
            this.array = new T[Math.Max(maxSize, MinCapacity) + 1];
        }

        // Properties
        public bool IsEmpty
        {
            get { return this.length == 0; }
        }

        public int Count
        {
            get { return this.length; }
        }
        
        public bool IsFull
        {
            get { return this.length+1 == this.array.Length; }
        }

        // Methods

        public void Insert(T value)
        {
            if (IsFull)
            {
                throw new Exception("Heap is full");
            }
            else
            {
                this.length++;
                this.array[this.length] = value;
                Rise(this.length);
            }
        }

        public T Peek()
        {
            if (IsEmpty)
            {
                throw new Exception("Heap is empty");
            }
            else
            {
                return this.array[1];
            }
        }

        public T Pop()
        {
            if (IsEmpty)
            {
                throw new Exception("Heap is empty");
            }
            else
            {
                T value = this.array[1];
                this.array[1] = this.array[this.length];
                this.length--;
                if (this.length > 0)
                {
                    this.array[1] = this.array[this.length + 1];
                    Sink(1);
                }
                return value;
            }
        }

        // Helper Methods
        private void Swap(int index1, int index2)
        {
            T temp = this.array[index1];
            this.array[index1] = this.array[index2];
            this.array[index2] = temp;
        }

        private void Rise(int index)
        {
            if (index > 1)
            {
                int parentIndex = index / 2;
                if (this.array[index].CompareTo(this.array[parentIndex]) > 0)
                {
                    Swap(index, parentIndex);
                    Rise(parentIndex);
                }
            }
        }

        private void Sink(int index)
        {
            T value = this.array[index];

            while (2*index <= this.length)
            {
                int largestChildIndex = GetLargestChildIndex(index);
                if (this.array[largestChildIndex].CompareTo(this.array[index]) <= 0)
                {
                    break;
                }
                this.array[index] = this.array[largestChildIndex];
                index = largestChildIndex;
            }
            this.array[index] = value;
        }
        private int GetLargestChildIndex(int index)
        {
            if (2*index == this.length || this.array[2*index].CompareTo(this.array[2*index+1]) > 0)
            {
                return index * 2;
            }
            else
            {
                return index * 2 + 1;
            }
        }

        // Class Methods

        public static MaxHeap<T> Heapify(T[] array)
        {
            MaxHeap<T> heap = new MaxHeap<T>(array.Length);
            heap.length = array.Length;
            for (int i = 0; i < array.Length; i++)
            {
                heap.array[i + 1] = array[i];
            }
            for (int i = array.Length; i >= 1; i--)
            {
                heap.Sink(i);
            }
            return heap;
        }

        public static T[] HeapSort(T[] array)
        {
            MaxHeap<T> heap = Heapify(array);
            T[] sortedArray = new T[array.Length];
            
            for (int i = array.Length - 1; i >= 0; i--)
            {
                sortedArray[i] = heap.Pop();
            }

            return sortedArray;
        }
    }
}