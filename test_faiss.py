#!/usr/bin/env python3
"""
Test script to verify FAISS installation and basic functionality.
"""

def test_faiss_import():
    """Test if FAISS can be imported successfully."""
    try:
        import faiss
        print("✓ FAISS imported successfully")
        return True
    except Exception as e:
        print(f"✗ FAISS import failed: {e}")
        return False

def test_langchain_faiss():
    """Test if LangChain FAISS integration works."""
    try:
        from langchain_community.vectorstores import FAISS
        from langchain_huggingface import HuggingFaceEmbeddings
        print("✓ LangChain FAISS import successful")
        return True
    except Exception as e:
        print(f"✗ LangChain FAISS import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic FAISS functionality."""
    try:
        from langchain_community.vectorstores import FAISS
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
        db = FAISS.from_documents(documents=docs, embedding=embedding)
        
        # Test similarity search
        results = db.similarity_search("test", k=1)
        
        print("✓ Basic FAISS functionality test passed")
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing FAISS installation and functionality...")
    print("=" * 50)
    
    tests = [
        test_faiss_import,
        test_langchain_faiss,
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
        print("✓ All tests passed! FAISS should work correctly.")
    else:
        print("✗ Some tests failed. Please check the error messages above.")
        print("\nTroubleshooting tips:")
        print("1. Try reinstalling FAISS: pip uninstall faiss-cpu && pip install faiss-cpu")
        print("2. Make sure you have the required dependencies: pip install numpy")
        print("3. Check if you're using a compatible Python version")

if __name__ == "__main__":
    main() 