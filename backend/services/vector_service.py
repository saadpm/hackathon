import os
import pickle
import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import settings


class VectorService:
    def __init__(self):
        # Use TfidfVectorizer - much lighter than sentence-transformers
        self.vectorizer = TfidfVectorizer(max_features=300, ngram_range=(1, 2))
        self.skill_vectors = None
        self.skill_metadata = {}
        self.skill_texts = []
        self.vector_db_path = settings.VECTOR_DB_PATH
        
        # Create vector store directory if it doesn't exist
        os.makedirs(self.vector_db_path, exist_ok=True)
        
        # Load existing index if available
        self.load_index()
    
    def create_skill_embedding(self, skill_text: str, proficiency: str = "", experience: float = 0) -> str:
        """
        Create embedding for a skill with context (lightweight version)
        """
        # Enrich skill text with context
        enriched_text = f"{skill_text} {proficiency} {experience}years"
        return enriched_text
    
    def add_skills_to_index(self, skills: List[Dict[str, any]]):
        """
        Add skills to index (lightweight TF-IDF version)
        skills format: [{"skill_name": "Python", "proficiency": "advanced", "experience": 3.5, "metadata": {...}}]
        """
        if not skills:
            return
        
        # Create text representations
        for skill in skills:
            skill_text = self.create_skill_embedding(
                skill.get("skill_name", ""),
                skill.get("proficiency", ""),
                skill.get("experience", 0)
            )
            skill_id = len(self.skill_texts)
            self.skill_texts.append(skill_text)
            self.skill_metadata[skill_id] = skill
        
        # Refit vectorizer with all skills
        if len(self.skill_texts) > 0:
            self.skill_vectors = self.vectorizer.fit_transform(self.skill_texts)
        
        # Save index
        self.save_index()
    
    def search_similar_skills(self, query_skill: str, k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Search for similar skills in the index
        Returns list of (skill_metadata, similarity_score) tuples
        """
        if self.skill_vectors is None or len(self.skill_texts) == 0:
            return []
        
        # Create query vector
        query_vector = self.vectorizer.transform([query_skill])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.skill_vectors)[0]
        
        # Get top k
        k = min(k, len(similarities))
        top_indices = np.argsort(similarities)[-k:][::-1]
        
        # Format results
        results = []
        for idx in top_indices:
            if idx in self.skill_metadata:
                results.append((self.skill_metadata[idx], float(similarities[idx])))
        
        return results
    
    def compare_skill_sets(
        self,
        employee_skills: List[Dict[str, any]],
        required_skills: List[str]
    ) -> Dict[str, any]:
        """
        Compare employee skills with required skills using TF-IDF
        Returns gap analysis
        """
        if not employee_skills or not required_skills:
            return {
                "missing_skills": required_skills,
                "matched_skills": [],
                "gap_percentage": 100.0,
                "similarity_scores": {}
            }
        
        # Create text representations
        employee_texts = [
            self.create_skill_embedding(
                s.get("skill_name", ""),
                s.get("proficiency", ""),
                s.get("experience", 0)
            )
            for s in employee_skills
        ]
        
        # Vectorize all skills together
        all_texts = employee_texts + required_skills
        vectorizer = TfidfVectorizer(max_features=300, ngram_range=(1, 2))
        vectors = vectorizer.fit_transform(all_texts)
        
        employee_vectors = vectors[:len(employee_skills)]
        required_vectors = vectors[len(employee_skills):]
        
        # Calculate similarities
        matched_skills = []
        missing_skills = []
        similarity_scores = {}
        
        for i, req_skill in enumerate(required_skills):
            req_vec = required_vectors[i:i+1]
            
            # Find best match in employee skills
            similarities = cosine_similarity(req_vec, employee_vectors)[0]
            best_idx = np.argmax(similarities)
            best_score = similarities[best_idx]
            
            similarity_scores[req_skill] = {
                "matched_skill": employee_skills[best_idx]["skill_name"],
                "similarity": float(best_score)
            }
            
            # Threshold for considering a match (0.5 = 50% similarity for TF-IDF)
            if best_score > 0.5:
                matched_skills.append(req_skill)
            else:
                missing_skills.append(req_skill)
        
        # Calculate gap percentage
        gap_percentage = (len(missing_skills) / len(required_skills)) * 100 if required_skills else 0
        
        return {
            "missing_skills": missing_skills,
            "matched_skills": matched_skills,
            "gap_percentage": round(gap_percentage, 2),
            "similarity_scores": similarity_scores
        }
    
    def save_index(self):
        """Save TF-IDF vectors and metadata to disk"""
        data = {
            'skill_texts': self.skill_texts,
            'skill_metadata': self.skill_metadata,
            'vectorizer': self.vectorizer if len(self.skill_texts) > 0 else None
        }
        
        with open(os.path.join(self.vector_db_path, "skills_data.pkl"), "wb") as f:
            pickle.dump(data, f)
    
    def load_index(self):
        """Load TF-IDF vectors and metadata from disk"""
        data_path = os.path.join(self.vector_db_path, "skills_data.pkl")
        
        if os.path.exists(data_path):
            with open(data_path, "rb") as f:
                data = pickle.load(f)
                self.skill_texts = data.get('skill_texts', [])
                self.skill_metadata = data.get('skill_metadata', {})
                saved_vectorizer = data.get('vectorizer')
                
                if saved_vectorizer and len(self.skill_texts) > 0:
                    self.vectorizer = saved_vectorizer
                    self.skill_vectors = self.vectorizer.transform(self.skill_texts)
    
    def clear_index(self):
        """Clear the index and metadata"""
        self.skill_texts = []
        self.skill_vectors = None
        self.skill_metadata = {}
        self.save_index()


# Singleton instance
vector_service = VectorService()

