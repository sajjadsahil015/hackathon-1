// @ts-check
import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A conceptual guide to building autonomous humanoid robots',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-github-username.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For local development use '/', for GitHub Pages use '/physical-ai-book/'
  baseUrl: '/',

  // GitHub pages deployment config
  organizationName: 'your-github-username',
  projectName: 'physical-ai-book',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // Enable Mermaid diagrams
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/',
          // Edit this page links
          editUrl: 'https://github.com/your-github-username/physical-ai-book/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Social card image
      image: 'img/social-card.png',

      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Physical AI Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'bookSidebar',
            position: 'left',
            label: 'Book',
          },
          {
            href: '/glossary',
            label: 'Glossary',
            position: 'left',
          },
          {
            href: 'https://github.com/your-github-username/physical-ai-book',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },

      footer: {
        style: 'dark',
        links: [
          {
            title: 'Book',
            items: [
              {
                label: 'Introduction',
                to: '/',
              },
              {
                label: 'Glossary',
                to: '/glossary',
              },
            ],
          },
          {
            title: 'Modules',
            items: [
              {
                label: 'Module 1: ROS 2',
                to: '/module-1-ros2/ros2-architecture',
              },
              {
                label: 'Module 2: Simulation',
                to: '/module-2-simulation/digital-twins-gazebo',
              },
              {
                label: 'Module 3: Isaac',
                to: '/module-3-isaac/perception-isaac-sim',
              },
              {
                label: 'Module 4: VLA',
                to: '/module-4-vla/vla-architecture',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'ROS 2 Documentation',
                href: 'https://docs.ros.org/en/humble/',
              },
              {
                label: 'NVIDIA Isaac',
                href: 'https://developer.nvidia.com/isaac',
              },
              {
                label: 'Nav2 Navigation',
                href: 'https://navigation.ros.org/',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI Book. Built with Docusaurus.`,
      },

      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'yaml', 'markup', 'json'],
      },

      // Mermaid configuration
      mermaid: {
        theme: { light: 'neutral', dark: 'dark' },
        options: {
          maxTextSize: 50000,
        },
      },

      // Table of contents
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 4,
      },

      // Algolia search (optional - configure if needed)
      // algolia: {
      //   appId: 'YOUR_APP_ID',
      //   apiKey: 'YOUR_SEARCH_API_KEY',
      //   indexName: 'physical-ai-book',
      // },
    }),
};

export default config;
