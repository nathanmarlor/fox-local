from bidirectional import FoxBidirectional


def main():
    """Main entry point"""
    fox_service = FoxBidirectional()
    fox_service.run()


if __name__ == "__main__":
    print("Starting Fox Local...")
    main()
