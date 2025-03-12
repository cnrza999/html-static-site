from textnode import TextNode, TextType

def main():
    # Create a TextNode with example values (you can use any values you want)
    node = TextNode("This is tidehunter", TextType.TEXT)
    sec_node = TextNode("Cherry tree", TextType.LINK, "https://love/cherrytree")
    # Print the node to see its string representation
    print(node)
    print(sec_node)

# Call the main function when the script runs
if __name__ == "__main__":
    main()