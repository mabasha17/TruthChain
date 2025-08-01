#!/usr/bin/env python3
"""
Test script to verify ChromaDB installation and basic functionality.
"""

def test_chromadb_import():
    """Test if ChromaDB can be imported successfully."""
    try:
        import chromadb
        print("✓ ChromaDB imported successfully")
        print(f"  Version: {chromadb.__version__}")
        return True
    except Exception as e:
        print(f"✗ ChromaDB import failed: {e}")
        return False

def test_langchain_chroma():
    """Test if LangChain Chroma integration works."""
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_huggingface import HuggingFaceEmbeddings
        print("✓ LangChain Chroma import successful")
        return True
    except Exception as e:
        print(f"✗ LangChain Chroma import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic ChromaDB functionality."""
    try:
        from langchain_community.vectorstores import Chroma
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain.schema import Document
        
        # Create a simple embedding
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Create a test document
        docs = [Document(page_content="This is a test document", metadata={"source": "test"})]
        
        # Create vector store
        db = Chroma.from_documents(documents=docs, embedding=embedding)
        
        # Test similarity search
        results = db.similarity_search("test", k=1)
        
        print("✓ Basic ChromaDB functionality test passed")
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing ChromaDB installation and functionality...")
    print("=" * 50)
    
    tests = [
        test_chromadb_import,
        test_langchain_chroma,
        test_basic_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! ChromaDB should work correctly.")
    else:
        print("✗ Some tests failed. Please check the error messages above.")
        print("\nTroubleshooting tips:")
        print("1. Try reinstalling ChromaDB: pip uninstall chromadb && pip install chromadb==0.4.22")
        print("2. Make sure you have the required dependencies: pip install hnswlib")
        print("3. Check if you're using a compatible Python version (3.8-3.11)")

if __name__ == "__main__":
    main() 