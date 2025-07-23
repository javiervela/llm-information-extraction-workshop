# example_usage.py
"""
Usage examples for the long text analysis module
Demonstrates different use cases and functionalities
"""

from interview_analyzer import InterviewAnalyzer
from long_text_analyzer import LongTextAnalyzer


def example_basic_text_analysis():
    """Basic example of long text analysis"""
    print("=" * 60)
    print("📝 EXAMPLE 1: Basic Long Text Analysis")
    print("=" * 60)

    # Sample text
    sample_text = """
    Artificial intelligence (AI) has experienced exponential growth in recent years,
    transforming entire industries and redefining the way we interact with technology.
    From recommendation systems used by platforms like Netflix and Amazon, to
    autonomous vehicles that promise to revolutionize transportation, AI has become an
    omnipresent force in our lives.
    
    Machine learning algorithms, especially deep neural networks, have demonstrated
    extraordinary capabilities in tasks that were previously considered exclusively human. 
    Natural language processing, image recognition, and complex decision-making are just 
    some of the areas where AI has shown superior performance.
    
    However, this progress does not come without challenges. Ethical concerns about algorithmic
    bias, data privacy, and the impact on employment are central topics in the current
    debate about AI. The need to develop responsible and transparent AI systems has become
    more urgent than ever.
    
    Looking to the future, we expect to see even more significant advances in areas such as
    artificial general intelligence (AGI), quantum computing applied to AI, and deeper
    integration of intelligent systems into our digital infrastructure. Collaboration between
    humans and machines will likely define the next era of technological innovation.
    """

    # Create analyzer
    analyzer = LongTextAnalyzer(model_name="llama3.1")

    try:
        # Perform analysis
        analysis = analyzer.analyze_text(sample_text)

        # Show results
        print(f"🎯 Keywords found: {len(analysis.keywords)}")
        print(f"   {', '.join(analysis.keywords[:5])}...")

        print(f"\n🏷️ Main topics: {len(analysis.key_topics)}")
        for i, topic in enumerate(analysis.key_topics[:3], 1):
            print(f"   {i}. {topic}")

        print(f"\n📊 Statistics:")
        print(f"   • Words: {analysis.word_count}")
        print(f"   • Reading time: {analysis.reading_time} min")
        print(f"   • Sentiment: {analysis.sentiment}")

        print(f"\n📋 Summary (first 150 characters):")
        print(f"   {analysis.summary[:150]}...")

    except Exception as e:
        print(f"❌ Error in analysis: {e}")


def example_interview_analysis():
    """Example of specialized interview analysis"""
    print("\n" + "=" * 60)
    print("🎤 EXAMPLE 2: Interview Analysis")
    print("=" * 60)

    # Sample interview transcript
    interview_text = """
    INTERVIEWER: Good morning, thank you very much for joining us. Could you start by telling us
    a bit about your professional background?
    
    CANDIDATE: Of course, thank you very much for the opportunity. I have approximately 8 years
    of experience in software development, mainly focused on web technologies.
    I started my career as a junior developer at a startup where I really learned the
    basics of agile development and the importance of teamwork.
    
    INTERVIEWER: Interesting. What motivated you to specialize in web technologies?
    
    CANDIDATE: Honestly, I'm fascinated by the ability to create solutions that can impact
    thousands of users. In my previous experience, we developed an application that helped
    small businesses manage their inventory, and seeing how that really improved their
    daily operations was incredibly rewarding.
    
    INTERVIEWER: What would you say has been your biggest professional challenge so far?
    
    CANDIDATE: Definitely when we had to migrate a legacy system that handled
    critical business data. The pressure was immense because we couldn't allow downtime.
    I learned a lot about planning, risk management, and the importance
    of having a solid contingency plan.
    
    INTERVIEWER: How do you keep up to date with new technologies?
    
    CANDIDATE: I'm very disciplined about this. I dedicate at least 2 hours a week to reading
    technical documentation, I actively participate in online communities like Stack Overflow
    and GitHub, and I try to implement small personal projects to experiment with
    new technologies before proposing them at work.
    
    INTERVIEWER: Excellent approach. What attracts you to this position specifically?
    
    CANDIDATE: I'm very excited about the opportunity to work with a team that clearly
    values innovation and technical excellence. Also, the fact that you are expanding
    your international presence presents unique scalability challenges that really motivate me
    to contribute.
    """

    # Create interview analyzer
    interview_analyzer = InterviewAnalyzer(model_name="llama3.1")

    try:
        # Perform specialized analysis
        analysis = interview_analyzer.analyze_interview(interview_text)

        # Show results
        print(f"🏷️ Interview type: {analysis.interview_type}")
        print(f"⏱️ Estimated duration: {analysis.duration_estimate} minutes")
        print(f"🤝 Interaction style: {analysis.interaction_style}")
        print(f"😊 Overall sentiment: {analysis.sentiment}")

        if analysis.speakers:
            print(f"\n👥 Identified participants:")
            for speaker in analysis.speakers:
                print(f"   • {speaker}")

        print(f"\n💡 Main insights:")
        for i, insight in enumerate(analysis.main_insights[:3], 1):
            print(f"   {i}. {insight}")

        print(f"\n💬 Highlighted quotes:")
        for i, quote in enumerate(analysis.quotes_highlights[:2], 1):
            print(f'   {i}. "{quote[:100]}..."')

        print(f"\n❓ Question/discussion topics:")
        for i, theme in enumerate(analysis.questions_themes, 1):
            print(f"   {i}. {theme}")

    except Exception as e:
        print(f"❌ Error in interview analysis: {e}")


def main():
    """Main function to run the examples"""
    example_basic_text_analysis()
    example_interview_analysis()


if __name__ == "__main__":
    main()
