import os

import pinecone
import streamlit as st

# load pinecone
pinecone.init(      
	api_key=st.secrets['PINECONE_API_KEY'],      
	environment='us-west1-gcp-free'      
)      

index_name = st.secrets['PINECONE_INDEX']

# Check if our index already exists. If it doesn't, we create it 
if index_name not in pinecone.list_indexes():
    # we create a new index
    # https://docs.pinecone.io/docs/choosing-index-type-and-size
    # using 1536 to match OPENAI Ada Embedding Model
    # using cosine as most common, see below for explination from ChatGPT
    pinecone.create_index(
      name=index_name,
      metric='cosine',
      dimension=1536  
    )
    print(f'🔥 {index_name} index create')
else:
  print(f'❌ {index_name} index already exists')



"""
When measuring similarity between vectors, such as those representing language embeddings in a Language Model (LLM), several distance metrics can be used. Each metric serves a different purpose and has its own characteristics. Let's compare cosine similarity, dot product similarity, and Euclidean distance:

1. **Cosine Similarity:**
   Cosine similarity measures the cosine of the angle between two vectors. It's often used to capture the direction of similarity rather than the magnitude. The cosine similarity ranges from -1 (opposite directions) to 1 (same direction), with 0 indicating orthogonality (no similarity).

   Formula:
   ```
   cosine_similarity(A, B) = (A dot B) / (||A|| * ||B||)
   ```

   Pros:
   - It's insensitive to vector magnitude, making it suitable for capturing semantic similarity.
   - It's commonly used in natural language processing for measuring text similarity.

   Cons:
   - It doesn't consider the magnitude of the vectors, so it might not fully capture differences in magnitudes.

2. **Dot Product Similarity:**
   The dot product measures the projection of one vector onto another. In some cases, the dot product can be used as a measure of similarity, though it's sensitive to vector magnitudes.

   Formula:
   ```
   dot_product_similarity(A, B) = A dot B
   ```

   Pros:
   - It's a simple calculation.
   - Can give an indication of how aligned the directions of the vectors are.

   Cons:
   - It doesn't take into account the vector magnitudes, which can be crucial in some cases.

3. **Euclidean Distance:**
   Euclidean distance measures the straight-line distance between two points in Euclidean space. It's often used to quantify the dissimilarity between vectors.

   Formula:
   ```
   euclidean_distance(A, B) = sqrt(sum((A[i] - B[i])^2 for i in range(len(A))))
   ```

   Pros:
   - It captures both direction and magnitude, giving a more complete similarity measure.
   - It can be useful when you want to consider both the direction and the distance.

   Cons:
   - It can be affected by vector length, so normalization might be necessary.

Which one to use depends on the context and the characteristics of your data:

- **Cosine Similarity** is widely used in NLP tasks, especially when comparing text embeddings where the magnitude isn't as important as the direction.

- **Dot Product Similarity** is simple and can be used when considering only alignment of vectors' directions, but it might not be ideal for capturing overall similarity.

- **Euclidean Distance** is useful when both direction and magnitude matter. However, if your vectors are of varying magnitudes, you might need to normalize them first.

In practice, a combination of these metrics along with experimentation is often used to determine which one provides the best results for a specific task.
"""