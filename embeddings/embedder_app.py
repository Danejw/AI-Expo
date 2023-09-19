



from embed import Emdedder


def main():
    
    embedder = Emdedder()

    embedder.run(csv_path=".\\links\\extracted_content.csv")

if __name__ == '__main__':
    main()

