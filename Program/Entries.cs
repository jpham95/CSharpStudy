namespace Entries
{
    public class StreamDay : IComparable<StreamDay>
    {
        public enum ComparisonType 
        { 
            AverageViewers,
            MaxViewers,
            Follows,
            MinsStreamed,
            MinsWatched,
            UniqueViewers,
            StreamedToWatchedRatio,
        };
        public ComparisonType Comparison { get; set; }
        public double? AverageViewers { get; set; }
        public int? MaxViewers { get; set; }
        public int? UniqueViewers { get; set; }
        public int? Follows { get; set; }
        public double? MinsStreamed { get; set; }
        public double? MinsWatched { get; set; }

        private double? watchedToStreamedRatio {
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


        public StreamDay(double AverageViewers, int MaxViewers, int UniqueViewers, int Follows, double MinsStreamed, double MinsWatched)
        {
            this.AverageViewers = AverageViewers;
            this.MaxViewers = MaxViewers;
            this.UniqueViewers = UniqueViewers;
            this.Follows = Follows;
            this.MinsStreamed = MinsStreamed;
            this.MinsWatched = MinsWatched;
            Comparison = ComparisonType.AverageViewers;
        }
        public int CompareTo(StreamDay? other)
        {
            if (other == null)
            {
                return 1;
            }
            // Compare based on the selected ComparisonType
            switch (Comparison)
            {
                case ComparisonType.AverageViewers:
                    // Compare AverageViewers property
                    return Nullable.Compare(AverageViewers, other.AverageViewers);
                case ComparisonType.MaxViewers:
                    // Compare MaxViewers property
                    return Nullable.Compare(MaxViewers, other.MaxViewers);
                case ComparisonType.Follows:
                    // Compare Follows property
                    return Nullable.Compare(Follows, other.Follows);
                case ComparisonType.MinsStreamed:
                    // Compare MinsStreamed property
                    return Nullable.Compare(MinsStreamed, other.MinsStreamed);
                case ComparisonType.MinsWatched:
                    // Compare MinsWatched property
                    return Nullable.Compare(MinsWatched, other.MinsWatched);
                case ComparisonType.UniqueViewers:
                    // Compare UniqueViewers property
                    return Nullable.Compare(UniqueViewers, other.UniqueViewers);
                case ComparisonType.StreamedToWatchedRatio:
                    // Compare streamedToWatchedRatio property
                    return Nullable.Compare(watchedToStreamedRatio, other.watchedToStreamedRatio);
                default:
                    // Invalid ComparisonType
                    throw new ArgumentException("Invalid ComparisonType");
            }
        }
    }
}