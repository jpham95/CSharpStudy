using System;
using DataStructures;
using System.IO;
using CsvHelper;
using System.Collections.Generic;
using Entries;
class Program
{
    static void Main(string[] args)
    {
        var bst = new BinarySearchTree<StreamDay>();
        using (var reader = new StreamReader("TwitchData.csv")) // Data omitted from repo
        using (var csv = new CsvReader(reader, System.Globalization.CultureInfo.InvariantCulture))
        {
            var records = new List<StreamDay>();

        }
    }
}
