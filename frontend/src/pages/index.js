import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HeroSection() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className={styles.heroTitle}>{siteConfig.title}</h1>
        <p className={styles.heroSubtitle}>{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Start Reading
          </Link>
          <Link
            className="button button--outline button--lg"
            to="/docs/glossary">
            View Glossary
          </Link>
        </div>
      </div>
    </header>
  );
}

const modules = [
  {
    title: 'Module 1: The Robotic Nervous System',
    icon: '🧠',
    description: 'Learn ROS 2 fundamentals - the communication backbone that connects all robot components through topics, services, and actions.',
    link: '/docs/module-1-ros2/ros2-architecture',
    color: '#2563eb',
  },
  {
    title: 'Module 2: The Digital Twin',
    icon: '🎮',
    description: 'Master simulation environments with Gazebo and Unity for safe robot development and testing.',
    link: '/docs/module-2-simulation/digital-twins-gazebo',
    color: '#16a34a',
  },
  {
    title: 'Module 3: The AI-Robot Brain',
    icon: '🤖',
    description: 'Explore NVIDIA Isaac for perception, Visual SLAM, and autonomous navigation with Nav2.',
    link: '/docs/module-3-isaac/perception-isaac-sim',
    color: '#9333ea',
  },
  {
    title: 'Module 4: Vision-Language-Action',
    icon: '🎯',
    description: 'Build autonomous humanoid robots with VLA architecture, voice control, and intelligent task planning.',
    link: '/docs/module-4-vla/vla-architecture',
    color: '#ea580c',
  },
];

function ModuleCard({ title, icon, description, link, color }) {
  return (
    <div className={styles.moduleCard} style={{ borderTopColor: color }}>
      <div className={styles.moduleIcon}>{icon}</div>
      <h3 className={styles.moduleTitle}>{title}</h3>
      <p className={styles.moduleDescription}>{description}</p>
      <Link className={styles.moduleLink} to={link} style={{ color }}>
        Explore Module →
      </Link>
    </div>
  );
}

function ModulesSection() {
  return (
    <section className={styles.modules}>
      <div className="container">
        <h2 className={styles.sectionTitle}>What You'll Learn</h2>
        <p className={styles.sectionSubtitle}>
          Four comprehensive modules taking you from robotics fundamentals to autonomous humanoid systems
        </p>
        <div className={styles.moduleGrid}>
          {modules.map((props, idx) => (
            <ModuleCard key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

const features = [
  {
    title: 'Conceptual Foundation',
    icon: '📚',
    description: 'Understand the "why" behind robotics concepts before diving into implementation details.',
  },
  {
    title: 'AI-Powered Assistant',
    icon: '💬',
    description: 'Ask questions about the book content using our integrated RAG chatbot.',
  },
  {
    title: 'Visual Learning',
    icon: '📊',
    description: 'Mermaid diagrams and tables help visualize complex robotics architectures.',
  },
  {
    title: 'Self-Assessment',
    icon: '✅',
    description: 'Success checks at the end of each chapter verify your understanding.',
  },
];

function FeatureCard({ title, icon, description }) {
  return (
    <div className={styles.featureCard}>
      <div className={styles.featureIcon}>{icon}</div>
      <h3 className={styles.featureTitle}>{title}</h3>
      <p className={styles.featureDescription}>{description}</p>
    </div>
  );
}

function FeaturesSection() {
  return (
    <section className={styles.features}>
      <div className="container">
        <h2 className={styles.sectionTitle}>Book Features</h2>
        <div className={styles.featureGrid}>
          {features.map((props, idx) => (
            <FeatureCard key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

function StatsSection() {
  return (
    <section className={styles.stats}>
      <div className="container">
        <div className={styles.statsGrid}>
          <div className={styles.statItem}>
            <div className={styles.statNumber}>4</div>
            <div className={styles.statLabel}>Modules</div>
          </div>
          <div className={styles.statItem}>
            <div className={styles.statNumber}>12</div>
            <div className={styles.statLabel}>Chapters</div>
          </div>
          <div className={styles.statItem}>
            <div className={styles.statNumber}>~10</div>
            <div className={styles.statLabel}>Hours of Content</div>
          </div>
          <div className={styles.statItem}>
            <div className={styles.statNumber}>100%</div>
            <div className={styles.statLabel}>Free & Open</div>
          </div>
        </div>
      </div>
    </section>
  );
}

function CTASection() {
  return (
    <section className={styles.cta}>
      <div className="container">
        <h2 className={styles.ctaTitle}>Ready to Build Autonomous Robots?</h2>
        <p className={styles.ctaDescription}>
          Start your journey into Physical AI and humanoid robotics today.
        </p>
        <Link
          className="button button--primary button--lg"
          to="/docs/intro">
          Get Started
        </Link>
      </div>
    </section>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title="Home"
      description={siteConfig.tagline}>
      <HeroSection />
      <main>
        <StatsSection />
        <ModulesSection />
        <FeaturesSection />
        <CTASection />
      </main>
    </Layout>
  );
}
