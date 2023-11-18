using System;
using System.IO;
using CsvHelper;
using System.Collections.Generic;
using CsvHelper.Configuration;
using System.Globalization;
using Entries;
class Program
{
    static void Main(string[] args)
    {
        var Data = new List<StreamDay>();
        Dictionary<string, StreamDay> DataDict = new Dictionary<string, StreamDay>();
        var config = new CsvConfiguration(CultureInfo.InvariantCulture)
        {
            PrepareHeaderForMatch = args => args.Header.Replace(" ", "") // Remove spaces from args
        };

        using (var reader = new StreamReader("Program/TwitchData.csv")) // Data omitted from repo
        using (var csv = new CsvReader(reader, config))
        {
            csv.Read();
            csv.ReadHeader();
            while (csv.Read())
            {
                var record = csv.GetRecord<StreamDay>();
                if (record != null)
                {
                    DataDict[record.Date] = record;
                    Data.Add(record);
                }
            }
        }
        foreach (var item in DataDict)
        {
            Console.WriteLine(item.Value);
        }
    }
}
