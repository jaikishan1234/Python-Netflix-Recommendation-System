
import math
from pathlib import Path

from src.model.movie import Movie
from src.model.movie_data import MovieData
from src.model.movie_match import MovieMatch


class MovieService:
    def __init__(self, embedding_model, json_mapper):
        self.embeddingModel = embedding_model
        self.jsonMapper = json_mapper
        self.moviesEmbedding = []

    def initializeMovies(self):
        self.moviesEmbedding.clear()

        resource = (
            Path(__file__).resolve().parents[1]
            / "data"
            / "movies_enriched.json"
        )

        with resource.open("r", encoding="utf-8") as input_stream:
            raw_movies = self.jsonMapper.load(input_stream)

        movie_data_list = []

        for data in raw_movies:
            movie_data = MovieData(
                title=data.get("title"),
                description=data.get("description"),
                release_year=data.get("release_year"),
                genres=data.get("genres"),
                original_language=data.get("original_language"),
                country=data.get("country"),
                runtime_minutes=data.get("runtime_minutes"),
                plot_summary=data.get("plot_summary"),
                themes=data.get("themes"),
                moods=data.get("moods"),
                tone=data.get("tone"),
                pacing=data.get("pacing"),
                story_complexity=data.get("story_complexity"),
                violence_level=data.get("violence_level"),
                romance_level=data.get("romance_level"),
                ending_type=data.get("ending_type"),
                content_warnings=data.get("content_warnings"),
                searchable_features=data.get("searchable_features"),
                metadata_status=data.get("metadata_status"),
            )

            movie_data_list.append(movie_data)

        for movie_data in movie_data_list:
            embedding_text = self.buildMovieText(movie_data)

            embedding = self.embeddingModel.embed(embedding_text)

            movie = Movie(
                title=movie_data.getTitle(),
                description=movie_data.getDescription(),
                embedding=embedding,
                release_year=movie_data.release_year,
                genres=movie_data.genres,
                original_language=movie_data.original_language,
                country=movie_data.country,
                runtime_minutes=movie_data.runtime_minutes,
                plot_summary=movie_data.plot_summary,
                themes=movie_data.themes,
                moods=movie_data.moods,
                tone=movie_data.tone,
                pacing=movie_data.pacing,
                story_complexity=movie_data.story_complexity,
                violence_level=movie_data.violence_level,
                romance_level=movie_data.romance_level,
                ending_type=movie_data.ending_type,
                content_warnings=movie_data.content_warnings,
                searchable_features=movie_data.searchable_features,
                metadata_status=movie_data.metadata_status,
            )

            self.moviesEmbedding.append(movie)

        print(
            str(len(self.moviesEmbedding))
            + " movies loaded with enriched embeddings."
        )

    def buildMovieText(self, movie_data):
        parts = []

        def add_text(label, value):
            if value is None or value == "":
                return

            if isinstance(value, list):
                value = ", ".join(
                    str(item) for item in value if item is not None
                )

            if value != "":
                parts.append(f"{label}: {value}")

        add_text("Movie title", movie_data.getTitle())
        add_text("Plot description", movie_data.getDescription())
        add_text("Plot summary", movie_data.plot_summary)
        add_text("Genres", movie_data.genres)
        add_text("Themes", movie_data.themes)
        add_text("Moods", movie_data.moods)
        add_text("Tone", movie_data.tone)
        add_text("Searchable features", movie_data.searchable_features)
        add_text("Release year", movie_data.release_year)
        add_text("Original language", movie_data.original_language)
        add_text("Country", movie_data.country)
        add_text("Runtime in minutes", movie_data.runtime_minutes)
        add_text("Pacing", movie_data.pacing)
        add_text("Story complexity", movie_data.story_complexity)
        add_text("Violence level", movie_data.violence_level)
        add_text("Romance level", movie_data.romance_level)
        add_text("Ending type", movie_data.ending_type)
        add_text("Content warnings", movie_data.content_warnings)

        return ". ".join(parts)

    def search(self, query):
        user_query_embedding = self.embeddingModel.embed(query)

        matches = []

        for movie in self.moviesEmbedding:
            similarity = self.cosineSimilarity(
                user_query_embedding,
                movie.getEmbedding(),
            )

            match = MovieMatch(
                movie.getTitle(),
                movie.getDescription(),
                similarity,
            )

            matches.append(match)

        self.sortBySimilarity(matches)

        return self.topKMatches(matches, 3)

    def similarMovies(self, title):
        selected_movie = self.findMovie(title)
        matches = []

        for movie in self.moviesEmbedding:
            if movie.getTitle().lower() == selected_movie.getTitle().lower():
                continue

            similarity = self.cosineSimilarity(
                selected_movie.getEmbedding(),
                movie.getEmbedding(),
            )

            match = MovieMatch(
                movie.getTitle(),
                movie.getDescription(),
                similarity,
            )

            matches.append(match)

        self.sortBySimilarity(matches)

        return self.topKMatches(matches, 3)

    def findMovie(self, title):
        for movie in self.moviesEmbedding:
            if movie.getTitle().lower() == title.strip().lower():
                return movie

        raise ValueError("Movie not found: " + title)

    def cosineSimilarity(self, a, b):
        if len(a) != len(b):
            raise ValueError(
                "Cannot compare embeddings with different dimensions."
            )

        dot_product = 0.0
        norm_a = 0.0
        norm_b = 0.0

        for i in range(len(a)):
            dot_product += a[i] * b[i]
            norm_a += a[i] * a[i]
            norm_b += b[i] * b[i]

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (math.sqrt(norm_a) * math.sqrt(norm_b))

    def sortBySimilarity(self, matches):
        matches.sort(
            key=lambda match: match.getMatch(),
            reverse=True,
        )

    def topKMatches(self, matches, limit):
        top_matches = []

        number_of_matches = min(limit, len(matches))

        for i in range(number_of_matches):
            top_matches.append(matches[i])

        return top_matches
