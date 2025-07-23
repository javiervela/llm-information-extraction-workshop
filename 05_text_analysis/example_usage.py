# example_usage.py
"""
Ejemplos de uso del módulo de análisis de textos largos
Demuestra diferentes casos de uso y funcionalidades
"""

import os
from pathlib import Path
from long_text_analyzer import LongTextAnalyzer
from interview_analyzer import InterviewAnalyzer


def example_basic_text_analysis():
    """Ejemplo básico de análisis de texto largo"""
    print("=" * 60)
    print("📝 EJEMPLO 1: Análisis Básico de Texto Largo")
    print("=" * 60)

    # Texto de ejemplo
    sample_text = """
    La inteligencia artificial (IA) ha experimentado un crecimiento exponencial en los últimos años,
    transformando industrias enteras y redefiniendo la manera en que interactuamos con la tecnología.
    Desde los sistemas de recomendación que utilizan plataformas como Netflix y Amazon, hasta los
    vehículos autónomos que prometen revolucionar el transporte, la IA se ha convertido en una
    fuerza omnipresente en nuestras vidas.
    
    Los algoritmos de machine learning, especialmente las redes neuronales profundas, han demostrado
    capacidades extraordinarias en tareas que antes se consideraban exclusivamente humanas. El
    procesamiento de lenguaje natural, el reconocimiento de imágenes, y la toma de decisiones
    complejas son solo algunas de las áreas donde la IA ha mostrado un rendimiento superior.
    
    Sin embargo, este progreso no viene sin desafíos. Las preocupaciones éticas sobre el sesgo
    algorítmico, la privacidad de los datos, y el impacto en el empleo son temas centrales en el
    debate actual sobre la IA. La necesidad de desarrollar sistemas de IA responsables y transparentes
    se ha vuelto más urgente que nunca.
    
    Mirando hacia el futuro, esperamos ver avances aún más significativos en áreas como la IA general
    artificial (AGI), la computación cuántica aplicada a la IA, y la integración más profunda de
    sistemas inteligentes en nuestra infraestructura digital. La colaboración entre humanos y
    máquinas probablemente definirá la próxima era de la innovación tecnológica.
    """

    # Crear analizador
    analyzer = LongTextAnalyzer(model_name="llama3.1")

    try:
        # Realizar análisis
        analysis = analyzer.analyze_text(sample_text)

        # Mostrar resultados
        print(f"🎯 Palabras clave encontradas: {len(analysis.keywords)}")
        print(f"   {', '.join(analysis.keywords[:5])}...")

        print(f"\n🏷️ Temas principales: {len(analysis.key_topics)}")
        for i, topic in enumerate(analysis.key_topics[:3], 1):
            print(f"   {i}. {topic}")

        print(f"\n📊 Estadísticas:")
        print(f"   • Palabras: {analysis.word_count}")
        print(f"   • Tiempo de lectura: {analysis.reading_time} min")
        print(f"   • Sentimiento: {analysis.sentiment}")

        print(f"\n📋 Resumen (primeras 150 caracteres):")
        print(f"   {analysis.summary[:150]}...")

    except Exception as e:
        print(f"❌ Error en el análisis: {e}")


def example_interview_analysis():
    """Ejemplo de análisis especializado de entrevista"""
    print("\n" + "=" * 60)
    print("🎤 EJEMPLO 2: Análisis de Entrevista")
    print("=" * 60)

    # Transcripción de entrevista de ejemplo
    interview_text = """
    ENTREVISTADOR: Buenos días, muchas gracias por acompañarnos. ¿Podrías comenzar contándonos
    un poco sobre tu trayectoria profesional?
    
    CANDIDATO: Por supuesto, muchas gracias por la oportunidad. Tengo aproximadamente 8 años
    de experiencia en desarrollo de software, principalmente enfocado en tecnologías web.
    Comencé mi carrera como desarrollador junior en una startup donde realmente aprendí las
    bases del desarrollo ágil y la importancia del trabajo en equipo.
    
    ENTREVISTADOR: Interesante. ¿Qué te motivó a especializarte en tecnologías web?
    
    CANDIDATO: La verdad es que me fascina la capacidad de crear soluciones que puedan impactar
    a miles de usuarios. En mi experiencia anterior, desarrollamos una aplicación que ayudaba
    a pequeñas empresas a gestionar su inventario, y ver cómo eso realmente mejoraba sus
    operaciones diarias fue increíblemente gratificante.
    
    ENTREVISTADOR: ¿Cuál dirías que ha sido tu mayor desafío profesional hasta ahora?
    
    CANDIDATO: Definitivamente fue cuando tuvimos que migrar un sistema legacy que manejaba
    datos críticos para el negocio. La presión era inmensa porque no podíamos permitir tiempo
    de inactividad. Aprendí muchísimo sobre planificación, gestión de riesgos, y la importancia
    de tener un plan de contingencia sólido.
    
    ENTREVISTADOR: ¿Cómo te mantienes actualizado con las nuevas tecnologías?
    
    CANDIDATO: Soy muy disciplinado con esto. Dedico al menos 2 horas semanales a leer
    documentación técnica, participo activamente en comunidades online como Stack Overflow
    y GitHub, y trato de implementar pequeños proyectos personales para experimentar con
    nuevas tecnologías antes de proponerlas en el trabajo.
    
    ENTREVISTADOR: Excelente enfoque. ¿Qué te atrae de esta posición específicamente?
    
    CANDIDATO: Me emociona mucho la oportunidad de trabajar con un equipo que claramente
    valora la innovación y la excelencia técnica. Además, el hecho de que estén expandiendo
    su presencia internacional presenta desafíos únicos de escalabilidad que realmente me
    motivan a contribuir.
    """

    # Crear analizador de entrevistas
    interview_analyzer = InterviewAnalyzer(model_name="llama3.1")

    try:
        # Realizar análisis especializado
        analysis = interview_analyzer.analyze_interview(interview_text)

        # Mostrar resultados
        print(f"🏷️ Tipo de entrevista: {analysis.interview_type}")
        print(f"⏱️ Duración estimada: {analysis.duration_estimate} minutos")
        print(f"🤝 Estilo de interacción: {analysis.interaction_style}")
        print(f"😊 Sentimiento general: {analysis.sentiment}")

        if analysis.speakers:
            print(f"\n👥 Participantes identificados:")
            for speaker in analysis.speakers:
                print(f"   • {speaker}")

        print(f"\n💡 Insights principales:")
        for i, insight in enumerate(analysis.main_insights[:3], 1):
            print(f"   {i}. {insight}")

        print(f"\n💬 Citas destacadas:")
        for i, quote in enumerate(analysis.quotes_highlights[:2], 1):
            print(f'   {i}. "{quote[:100]}..."')

        print(f"\n❓ Temas de preguntas/discusión:")
        for i, theme in enumerate(analysis.questions_themes, 1):
            print(f"   {i}. {theme}")

    except Exception as e:
        print(f"❌ Error en el análisis de entrevista: {e}")


def main():
    """Función principal para ejecutar los ejemplos"""
    example_basic_text_analysis()
    example_interview_analysis()


if __name__ == "__main__":
    main()
