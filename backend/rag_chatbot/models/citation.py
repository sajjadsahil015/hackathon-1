"""Citation models for source attribution."""

from pydantic import BaseModel, Field


class Citation(BaseModel):
    """A reference to a specific location in the book."""

    chapter_number: int = Field(..., ge=1, description="Chapter number (1-based)")
    chapter_title: str = Field(..., description="Title of the chapter")
    section_number: int | None = Field(None, ge=1, description="Section number within chapter")
    section_title: str | None = Field(None, description="Title of the section")
    page_start: int = Field(..., ge=1, description="Starting page number")
    page_end: int = Field(..., ge=1, description="Ending page number")
    relevance_score: float = Field(
        ..., ge=0.0, le=1.0, description="Relevance score (0.0 to 1.0)"
    )

    def format_reference(self) -> str:
        """Format citation as a readable reference string."""
        parts = [f"Chapter {self.chapter_number}: {self.chapter_title}"]
        if self.section_number and self.section_title:
            parts.append(f"Section {self.section_number}: {self.section_title}")
        parts.append(f"(pp. {self.page_start}-{self.page_end})")
        return ", ".join(parts)
