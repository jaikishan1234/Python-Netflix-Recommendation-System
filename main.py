
from src.demo_application import DemoApplication
from src.embedding_model import EmbeddingModel


def main():
    embedding_model = EmbeddingModel()
    controller = DemoApplication.main(embedding_model)

    while True:
        print("\n=== Movie Recommendation System ===")
        print("1. Search movies by description")
        print("2. Find similar movies")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            query = input("Describe the movie you're looking for: ").strip()

            if not query:
                print("Please enter a description.")
                continue

            matches = controller.search(query)

        elif choice == "2":
            title = input("Enter a movie title: ").strip()

            if not title:
                print("Please enter a movie title.")
                continue

            try:
                matches = controller.similarMovies(title)
            except ValueError as error:
                print(error)
                continue

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")
            continue

        print("\nTop recommendations:")

        if not matches:
            print("No matching movies found.")
            continue

        for index, match in enumerate(matches, start=1):
            print(f"\n{index}. {match.getTitle()}")
            print(f"   Description: {match.getDescription()}")
            print(f"   Similarity: {match.getMatch():.4f}")


if __name__ == "__main__":
    main()
