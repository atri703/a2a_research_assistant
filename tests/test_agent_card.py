from app.a2a.service import get_agent_card

def test_agent_card_has_research_skill():
    card = get_agent_card()
    assert card["name"] == "Research Supervisor"
    assert any(skill["id"] == "research-paper" for skill in card["skills"])
