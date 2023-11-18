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
        public double? MinutesStreamed { get; set; }
        public double? MinutesWatched { get; set; }

        public double? watchedToStreamedRatio {
            get {
                if (MinutesStreamed == null || MinutesWatched == null)
                {
                    return null;
                }
                else
                {
                    return MinutesWatched / MinutesStreamed;
                }
            }
        }


        public StreamDay(string Date, double AverageViewers, int MaxViewers, int UniqueViewers, int Follows, double MinutesStreamed, double MinutesWatched)
        {
            this.Date = Date;
            this.AverageViewers = AverageViewers;
            this.MaxViewers = MaxViewers;
            this.UniqueViewers = UniqueViewers;
            this.Follows = Follows;
            this.MinutesStreamed = MinutesStreamed;
            this.MinutesWatched = MinutesWatched;
            Property = SelectedProperty.AverageViewers;
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
                    return Nullable.Compare(MinutesStreamed, other.MinutesStreamed);
                case SelectedProperty.MinsWatched:
                    // Compare MinsWatched property
                    return Nullable.Compare(MinutesWatched, other.MinutesWatched);
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
        
        public override string ToString()
        {
            return $"Stream on {this.Date}";
        }
    }
}