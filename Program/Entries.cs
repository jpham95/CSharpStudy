namespace Entries
{
    public class StreamDay : IComparable<StreamDay>
    {
        public enum SelectedProperty 
        { 
            AverageViewers,
            MaxViewers,
            Follows,
            MinsStreamed,
            MinsWatched,
            UniqueViewers,
            StreamedToWatchedRatio,
        };

        public string Date { get; set; }
        public SelectedProperty Property { get; set; }
        public double? AverageViewers { get; set; }
        public int? MaxViewers { get; set; }
        public int? UniqueViewers { get; set; }
        public int? Follows { get; set; }
        public double? MinsStreamed { get; set; }
        public double? MinsWatched { get; set; }

        public double? watchedToStreamedRatio {
            get {
                if (MinsStreamed == null || MinsWatched == null)
                {
                    return null;
                }
                else
                {
                    return MinsWatched / MinsStreamed;
                }
            }
        }


        public StreamDay(string Date, double AverageViewers, int MaxViewers, int UniqueViewers, int Follows, double MinsStreamed, double MinsWatched)
        {
            this.Date = Date;
            this.AverageViewers = AverageViewers;
            this.MaxViewers = MaxViewers;
            this.UniqueViewers = UniqueViewers;
            this.Follows = Follows;
            this.MinsStreamed = MinsStreamed;
            this.MinsWatched = MinsWatched;
            Property = SelectedProperty.AverageViewers;

            Dictionary<string, object?> properties = new Dictionary<string, object?>()
            {
                { "AverageViewers", AverageViewers },
                { "MaxViewers", MaxViewers },
                { "Follows", Follows },
                { "MinsStreamed", MinsStreamed },
                { "MinsWatched", MinsWatched },
                { "UniqueViewers", UniqueViewers },
                { "StreamedToWatchedRatio", watchedToStreamedRatio },
            };
        }
        public int CompareTo(StreamDay? other)
        {
            if (other == null)
            {
                return 1;
            }
            // Compare based on the selected ComparisonType
            switch (Property)
            {
                case SelectedProperty.AverageViewers:
                    // Compare AverageViewers property
                    return Nullable.Compare(AverageViewers, other.AverageViewers);
                case SelectedProperty.MaxViewers:
                    // Compare MaxViewers property
                    return Nullable.Compare(MaxViewers, other.MaxViewers);
                case SelectedProperty.Follows:
                    // Compare Follows property
                    return Nullable.Compare(Follows, other.Follows);
                case SelectedProperty.MinsStreamed:
                    // Compare MinsStreamed property
                    return Nullable.Compare(MinsStreamed, other.MinsStreamed);
                case SelectedProperty.MinsWatched:
                    // Compare MinsWatched property
                    return Nullable.Compare(MinsWatched, other.MinsWatched);
                case SelectedProperty.UniqueViewers:
                    // Compare UniqueViewers property
                    return Nullable.Compare(UniqueViewers, other.UniqueViewers);
                case SelectedProperty.StreamedToWatchedRatio:
                    // Compare streamedToWatchedRatio property
                    return Nullable.Compare(watchedToStreamedRatio, other.watchedToStreamedRatio);
                default:
                    // Invalid ComparisonType
                    throw new ArgumentException("Invalid ComparisonType");
            }
        }
        
        private T GetComparisonValue<T>()
        {
            throw new NotImplementedException();
        }
        public override string ToString()
        {
            string output = "";
            foreach (SelectedProperty comparisonType in Enum.GetValues(typeof(SelectedProperty)))
            {
                output += $"{comparisonType}: ";
            }
            throw new NotImplementedException();
        }
    }
}