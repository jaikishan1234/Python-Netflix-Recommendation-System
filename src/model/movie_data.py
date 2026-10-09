
class MovieData:
    def __init__(
        self,
        title=None,
        description=None,
        release_year=None,
        genres=None,
        original_language=None,
        country=None,
        runtime_minutes=None,
        plot_summary=None,
        themes=None,
        moods=None,
        tone=None,
        pacing=None,
        story_complexity=None,
        violence_level=None,
        romance_level=None,
        ending_type=None,
        content_warnings=None,
        searchable_features=None,
        metadata_status=None,
    ):
        self.title = title
        self.description = description
        self.release_year = release_year
        self.genres = genres if genres is not None else []
        self.original_language = original_language
        self.country = country
        self.runtime_minutes = runtime_minutes
        self.plot_summary = plot_summary
        self.themes = themes if themes is not None else []
        self.moods = moods if moods is not None else []
        self.tone = tone
        self.pacing = pacing
        self.story_complexity = story_complexity
        self.violence_level = violence_level
        self.romance_level = romance_level
        self.ending_type = ending_type
        self.content_warnings = (
            content_warnings if content_warnings is not None else []
        )
        self.searchable_features = (
            searchable_features
            if searchable_features is not None
            else []
        )
        self.metadata_status = metadata_status

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getDescription(self):
        return self.description

    def setDescription(self, description):
        self.description = description
