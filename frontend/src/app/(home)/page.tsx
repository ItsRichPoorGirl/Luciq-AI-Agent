'use client';

import { useEffect, useState, useRef } from 'react';
import { motion, usePresence } from 'framer-motion';

export default function HomePage() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
    const heroRef = useRef<HTMLElement>(null);

    useEffect(() => {
          setIsLoaded(true);
    }, []);

    useEffect(() => {
          const handleMouseMove = (e: MouseEvent) => {
                  setMousePosition({ x: e.clientX, y: e.clientY });
          };
          window.addEventListener('mousemove', handleMouseMove);
          return () => window.removeEventListener('mousemove', handleMouseMove);
    }, []);

    const companies = ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix', 'Spotify', 'Stripe'];

    const features = [
      { icon: '⚡', title: 'AI-Powered Automation', desc: 'Automate complex workflows with intelligent AI that learns and adapts.', color: 'from-violet-500 to-purple-500' },
      { icon: '📄', title: 'Smart Documents', desc: 'Extract insights and generate reports from documents instantly.', color: 'from-blue-500 to-cyan-500' },
      { icon: '📊', title: 'Advanced Analytics', desc: 'Transform data into beautiful visualizations and insights.', color: 'from-purple-500 to-pink-500' },
      { icon: '💬', title: 'Natural Language', desc: 'Communicate in plain English and get intelligent responses.', color: 'from-pink-500 to-rose-500' },
      { icon: '🔗', title: 'Seamless Integrations', desc: 'Connect with 200+ tools for a unified workflow.', color: 'from-cyan-500 to-teal-500' },
      { icon: '🔔', title: 'Smart Notifications', desc: 'AI-powered alerts that prioritize what matters most.', color: 'from-orange-500 to-amber-500' },
        ];

    const testimonials = [
      { name: 'Sarah Johnson', role: 'Data Scientist at TechCorp', quote: 'Luciq AI has completely transformed how our team handles data analysis. What used to take days now takes minutes, and the insights are far more comprehensive.', metrics: { saved: '85%', insights: '3x' } },
      { name: 'Michael Chen', role: 'Product Manager', quote: 'The natural language processing capabilities are mind-blowing. I can ask complex questions and get insightful answers immediately.' },
      { name: 'Emily Rodriguez', role: 'Content Strategist', quote: 'As a content creator, Luciq AI has been a game-changer. It helps me brainstorm ideas and refine my writing effortlessly.' },
      { name: 'David Park', role: 'CTO at StartupXYZ', quote: 'The integration capabilities are seamless. Our entire tech stack works together like never before.' },
        ];

    const pricingPlans = [
      { name: 'Free', price: '$0', period: '/month', desc: 'Perfect for trying out Luciq AI', features: ['30 minutes of usage', 'Basic AI model', 'Public projects only', 'Community support'], cta: 'Get Started Free', popular: false },
      { name: 'Pro', price: '$20', period: '/month', desc: 'For professionals and small teams', features: ['2 hours of usage', 'Intelligent AI model', 'Private projects', 'Full Luciq capabilities', 'Priority support'], cta: 'Start Free Trial', popular: true },
      { name: 'Enterprise', price: 'Custom', period: '', desc: 'For organizations with advanced needs', features: ['Unlimited usage', 'Custom AI training', 'Advanced integrations', 'Dedicated support', 'SLA guarantee'], cta: 'Contact Sales', popular: false },
        ];

    const steps = [
      { num: '01', title: 'Connect Your Tools', desc: 'Integrate with your existing workflow tools in one click. We support 200+ popular applications.', icon: '🔗' },
      { num: '02', title: 'Train Your AI', desc: 'Luciq AI learns from your patterns and preferences to deliver personalized automation.', icon: '🧠' },
      { num: '03', title: 'Automate & Scale', desc: 'Watch your productivity soar as Luciq AI handles repetitive tasks and surfaces insights.', icon: '✓' },
        ];

    return (
          <div className="min-h-screen bg-[#0a0a0f] text-white overflow-hidden">
            {/* Background Effects */}
                <div className="fixed inset-0 z-0">
                        <div className="absolute top-[-200px] left-[-100px] w-[600px] h-[600px] rounded-full bg-gradient-to-br from-violet-500/20 to-transparent blur-[80px] animate-pulse" />
                        <div className="absolute top-1/2 right-[-150px] w-[500px] h-[500px] rounded-full bg-gradient-to-br from-pink-500/15 to-transparent blur-[80px] animate-pulse" style={{ animationDelay: '2s' }} />
                        <div className="absolute bottom-[-100px] left-1/3 w-[400px] h-[400px] rounded-full bg-gradient-to-br from-cyan-500/15 to-transparent blur-[80px] animate-pulse" style={{ animationDelay: '4s' }} />
                        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:80px_80px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,black_40%,transparent_100%)]" />
                </div>div>
          
            {/* Navigation */}
                <nav className="fixed top-0 left-0 right-0 z-50 px-6 py-4">
                        <div className="max-w-7xl mx-auto flex items-center justify-between">
                                  <div className="flex items-center gap-2">
                                              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center">
                                                            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                                                            <path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
                                                                            <circle cx="12" cy="12" r="10" />
                                                            </svg>svg>
                                              </div>div>
                                              <span className="text-xl font-bold">Luciq<span className="bg-gradient-to-r from-violet-400 to-pink-400 bg-clip-text text-transparent">AI</span>span></span>span>
                                  </div>div>
                                  <div className="hidden md:flex items-center gap-8">
                                    {['Features', 'How it Works', 'Testimonials', 'Pricing'].map((item) => (
                          <a key={item} href={`#${item.toLowerCase().replace(' ', '-')}`} className="text-white/60 hover:text-white text-sm font-medium transition-colors relative group">
                            {item}
                                          <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-violet-500 to-pink-500 group-hover:w-full transition-all duration-300" />
                          </a>a>
                        ))}
                                  </div>div>
                                  <div className="flex items-center gap-4">
                                              <button className="text-white/60 hover:text-white text-sm font-medium transition-colors">Sign In</button>button>
                                              <button className="px-5 py-2.5 bg-gradient-to-r from-violet-600 to-purple-600 rounded-xl text-sm font-semibold hover:shadow-lg hover:shadow-violet-500/25 hover:-translate-y-0.5 transition-all duration-300">
                                                            Get Started
                                                            <svg className="w-4 h-4 inline ml-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                                                            <path d="M5 12h14M12 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round" />
                                                            </svg>svg>
                                              </button>button>
                                  </div>div>
                        </div>div>
                </nav>nav>
          
            {/* Hero Section */}
                <section ref={heroRef} className="relative z-10 min-h-screen flex items-center pt-24 pb-16 px-6">
                        <div className="max-w-7xl mx-auto w-full grid lg:grid-cols-2 gap-12 items-center">
                                  <motion.div
                                                initial={{ opacity: 0, y: 40 }}
                                                animate={isLoaded ? { opacity: 1, y: 0 } : {}}
                                                transition={{ duration: 0.8, ease: 'easeOut' }}
                                              >
                                              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-violet-500/10 border border-violet-500/20 mb-8">
                                                            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                                                            <span className="text-sm text-white/70">Introducing the Future of AI Automation</span>span>
                                                            <span className="text-violet-400">→</span>span>
                                              </div>div>
                                  
                                              <h1 className="text-5xl lg:text-7xl font-bold leading-[1.1] mb-6 font-display">
                                                            <span className="block">Transform Your</span>span>
                                                            <span className="block bg-gradient-to-r from-violet-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent bg-[length:200%_200%] animate-gradient">Workflow with AI</span>span>
                                                            <span className="block">Intelligence</span>span>
                                              </h1>h1>
                                  
                                              <p className="text-lg text-white/60 leading-relaxed mb-10 max-w-xl">
                                                            Luciq AI combines cutting-edge artificial intelligence with an intuitive interface to automate tasks, analyze data, and unlock insights at unprecedented speed.
                                              </p>p>
                                  
                                              <div className="flex flex-col sm:flex-row gap-4 mb-12">
                                                            <div className="flex-1 flex items-center gap-3 px-4 py-3 rounded-2xl bg-white/[0.03] border border-white/10 focus-within:border-violet-500/50 focus-within:shadow-[0_0_0_4px_rgba(139,92,246,0.1)] transition-all">
                                                                            <svg className="w-5 h-5 text-white/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                                                                              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" strokeLinecap="round" strokeLinejoin="round" />
                                                                            </svg>svg>
                                                                            <input type="text" placeholder="Ask Luciq AI anything..." className="flex-1 bg-transparent text-white placeholder-white/40 outline-none" />
                                                                            <button className="p-2.5 rounded-xl bg-gradient-to-r from-violet-600 to-purple-600 hover:scale-105 transition-transform">
                                                                                              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                                                                                                  <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" strokeLinecap="round" strokeLinejoin="round" />
                                                                                                </svg>svg>
                                                                            </button>button>
                                                            </div>div>
                                              </div>div>
                                  
                                              <div className="flex flex-wrap gap-4 mb-12">
                                                            <button className="px-8 py-4 bg-gradient-to-r from-violet-600 to-purple-600 rounded-2xl font-semibold hover:shadow-xl hover:shadow-violet-500/25 hover:-translate-y-1 transition-all duration-300 relative overflow-hidden group">
                                                                            <span className="relative z-10">Start Free Trial</span>span>
                                                                            <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
                                                            </button>button>
                                                            <button className="px-8 py-4 rounded-2xl border border-white/20 font-medium hover:bg-white/5 transition-all flex items-center gap-3">
                                                                            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                                                                                              <path d="M8 5v14l11-7z" />
                                                                            </svg>svg>
                                                                            Watch Demo
                                                            </button>button>
                                              </div>div>
                                  
                                              <div className="flex items-center gap-8 pt-8 border-t border-white/10">
                                                {[{ value: '50K+', label: 'Active Users' }, { value: '99.9%', label: 'Uptime SLA' }, { value: '10M+', label: 'Tasks Automated' }].map((stat, i) => (
                                                                <div key={i} className="flex flex-col">
                                                                                  <span className="text-2xl lg:text-3xl font-bold bg-gradient-to-b from-white to-white/70 bg-clip-text text-transparent">{stat.value}</span>span>
                                                                                  <span className="text-sm text-white/50">{stat.label}</span>span>
                                                                </div>div>
                                                              ))}
                                              </div>div>
                                  </motion.div>motion.div>
                        
                          {/* Hero Visual */}
                                  <motion.div
                                                className="relative flex items-center justify-center"
                                                initial={{ opacity: 0, scale: 0.8 }}
                                                animate={isLoaded ? { opacity: 1, scale: 1 } : {}}
                                                transition={{ duration: 1, ease: 'easeOut', delay: 0.2 }}
                                              >
                                              <div className="absolute w-[400px] h-[400px] rounded-full bg-gradient-to-br from-violet-500/30 to-pink-500/20 blur-3xl" />
                                              
                                    {/* AI Orb */}
                                              <div className="relative w-72 h-72">
                                                            <div className="absolute inset-0 rounded-full border border-violet-500/30 animate-[spin_20s_linear_infinite]" />
                                                            <div className="absolute inset-4 rounded-full border border-pink-500/20 animate-[spin_15s_linear_infinite_reverse]" />
                                                            <div className="absolute inset-8 rounded-full border border-cyan-500/15 animate-[spin_10s_linear_infinite]" />
                                                            <div className="absolute inset-16 rounded-full bg-gradient-to-br from-violet-500 via-pink-500 to-cyan-500 shadow-[0_0_60px_rgba(139,92,246,0.5),0_0_120px_rgba(236,72,153,0.3)] animate-pulse" />
                                              </div>div>
                                  
                                    {/* Floating Cards */}
                                    {[
                                                { top: '5%', right: '0', icon: '⚡', label: 'Task Automated', value: '+847', delay: 0 },
                                                { bottom: '30%', left: '-10%', icon: '📈', label: 'Efficiency', value: '+92%', delay: 0.5 },
                                                { bottom: '5%', right: '5%', icon: '⏱️', label: 'Time Saved', value: '12h/week', delay: 1 },
                                                            ].map((card, i) => (
                                                                            <motion.div
                                                                                              key={i}
                                                                                              className="absolute px-5 py-3 rounded-2xl bg-[#0f0f19]/90 backdrop-blur-xl border border-white/10 flex items-center gap-3 shadow-xl"
                                                                                              style={{ top: card.top, right: card.right, bottom: card.bottom, left: card.left }}
                                                                                              initial={{ opacity: 0, y: 20 }}
                                                                                              animate={isLoaded ? { opacity: 1, y: 0 } : {}}
                                                                                              transition={{ duration: 0.6, delay: 0.5 + card.delay }}
                                                                                            >
                                                                                            <span className="text-2xl">{card.icon}</span>span>
                                                                                            <div>
                                                                                                              <p className="text-xs text-white/50">{card.label}</p>p>
                                                                                                              <p className="text-lg font-bold text-white">{card.value}</p>p>
                                                                                              </div>div>
                                                                            </motion.div>motion.div>
                                                                          ))}
                                  </motion.div>motion.div>
                        </div>div>
                </section>section>
          
            {/* Trusted By Section */}
                <section className="relative z-10 py-16 border-y border-white/5">
                        <div className="max-w-7xl mx-auto px-6">
                                  <p className="text-center text-white/40 text-sm uppercase tracking-widest mb-8">Trusted by World-Class Teams</p>p>
                                  <div className="flex items-center justify-center gap-12 flex-wrap opacity-50">
                                    {companies.map((company, i) => (
                          <span key={i} className="text-xl font-semibold text-white/60 hover:text-white transition-colors">{company}</span>span>
                        ))}
                                  </div>div>
                        </div>div>
                </section>section>
          
            {/* Features Section */}
                <section id="features" className="relative z-10 py-24 px-6">
                        <div className="max-w-7xl mx-auto">
                                  <div className="text-center mb-16">
                                              <span className="inline-block px-4 py-2 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-400 text-sm font-medium mb-4">FEATURES</span>span>
                                              <h2 className="text-4xl lg:text-5xl font-bold mb-6">
                                                            Everything you need to<br />
                                                            <span className="bg-gradient-to-r from-violet-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">supercharge productivity</span>span>
                                              </h2>h2>
                                              <p className="text-white/60 max-w-2xl mx-auto">
                                                            Powerful AI capabilities designed to transform how you work, create, and analyze.
                                              </p>p>
                                  </div>div>
                        
                                  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {features.map((feature, i) => (
                          <motion.div
                                            key={i}
                                            className="group p-8 rounded-3xl bg-white/[0.02] border border-white/10 hover:border-violet-500/30 hover:bg-white/[0.04] transition-all duration-300"
                                            initial={{ opacity: 0, y: 20 }}
                                            whileInView={{ opacity: 1, y: 0 }}
                                            viewport={{ once: true }}
                                            transition={{ delay: i * 0.1 }}
                                          >
                                          <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${feature.color} flex items-center justify-center text-2xl mb-6`}>
                                            {feature.icon}
                                          </div>div>
                                          <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>h3>
                                          <p className="text-white/60 mb-4">{feature.desc}</p>p>
                                          <a href="#" className="text-violet-400 text-sm font-medium inline-flex items-center gap-1 group-hover:gap-2 transition-all">
                                                            Learn more <span>→</span>span>
                                          </a>a>
                          </motion.div>motion.div>
                        ))}
                                  </div>div>
                        </div>div>
                </section>section>
          
            {/* How It Works Section */}
                <section id="how-it-works" className="relative z-10 py-24 px-6">
                        <div className="max-w-7xl mx-auto">
                                  <div className="text-center mb-16">
                                              <span className="inline-block px-4 py-2 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-400 text-sm font-medium mb-4">HOW IT WORKS</span>span>
                                              <h2 className="text-4xl lg:text-5xl font-bold mb-6">
                                                            Get started in <span className="bg-gradient-to-r from-violet-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">3 simple steps</span>span>
                                              </h2>h2>
                                              <p className="text-white/60 max-w-2xl mx-auto">
                                                            From signup to AI-powered productivity in minutes.
                                              </p>p>
                                  </div>div>
                        
                                  <div className="space-y-6">
                                    {steps.map((step, i) => (
                          <motion.div
                                            key={i}
                                            className="flex items-center gap-8"
                                            initial={{ opacity: 0, x: -20 }}
                                            whileInView={{ opacity: 1, x: 0 }}
                                            viewport={{ once: true }}
                                            transition={{ delay: i * 0.2 }}
                                          >
                                          <div className="flex flex-col items-center">
                                                            <span className={`text-sm font-bold ${i === 0 ? 'text-violet-400' : i === 1 ? 'text-cyan-400' : 'text-pink-400'}`}>{step.num}</span>span>
                                            {i < steps.length - 1 && <div className={`w-0.5 h-20 ${i === 0 ? 'bg-gradient-to-b from-violet-400 to-cyan-400' : 'bg-gradient-to-b from-cyan-400 to-pink-400'}`} />}
                                          </div>div>
                                          <div className="flex-1 p-6 rounded-2xl bg-white/[0.02] border border-white/10">
                                                            <h3 className="text-xl font-semibold mb-2">{step.title}</h3>h3>
                                                            <p className="text-white/60">{step.desc}</p>p>
                                          </div>div>
                                          <div className={`w-14 h-14 rounded-2xl ${i === 0 ? 'bg-violet-500/20 text-violet-400' : i === 1 ? 'bg-cyan-500/20 text-cyan-400' : 'bg-pink-500/20 text-pink-400'} flex items-center justify-center text-2xl`}>
                                            {step.icon}
                                          </div>div>
                          </motion.div>motion.div>
                        ))}
                                  </div>div>
                        </div>div>
                </section>section>
          
            {/* Testimonials Section */}
                <section id="testimonials" className="relative z-10 py-24 px-6">
                        <div className="max-w-7xl mx-auto">
                                  <div className="text-center mb-16">
                                              <span className="inline-block px-4 py-2 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-400 text-sm font-medium mb-4">TESTIMONIALS</span>span>
                                              <h2 className="text-4xl lg:text-5xl font-bold mb-6">
                                                            Loved by <span className="bg-gradient-to-r from-violet-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">industry leaders</span>span>
                                              </h2>h2>
                                              <p className="text-white/60 max-w-2xl mx-auto">
                                                            See what our customers have to say about their experience with Luciq AI.
                                              </p>p>
                                  </div>div>
                        
                                  <div className="grid md:grid-cols-2 gap-6">
                                    {testimonials.map((testimonial, i) => (
                          <motion.div
                                            key={i}
                                            className="p-8 rounded-3xl bg-white/[0.02] border border-white/10"
                                            initial={{ opacity: 0, y: 20 }}
                                            whileInView={{ opacity: 1, y: 0 }}
                                            viewport={{ once: true }}
                                            transition={{ delay: i * 0.1 }}
                                          >
                                          <div className="text-violet-400 text-4xl mb-4">"</div>div>
                                          <p className="text-white/80 italic mb-6">{testimonial.quote}</p>p>
                                          <div className="flex items-center gap-4">
                                                            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-violet-500 to-pink-500" />
                                                            <div>
                                                                                <p className="font-semibold">{testimonial.name}</p>p>
                                                                                <p className="text-sm text-white/50">{testimonial.role}</p>p>
                                                            </div>div>
                                          </div>div>
                            {testimonial.metrics && (
                                                              <div className="flex gap-8 mt-6 pt-6 border-t border-white/10">
                                                                                  <div>
                                                                                                        <p className="text-2xl font-bold text-violet-400">{testimonial.metrics.saved}</p>p>
                                                                                                        <p className="text-sm text-white/50">Time saved</p>p>
                                                                                    </div>div>
                                                                                  <div>
                                                                                                        <p className="text-2xl font-bold text-cyan-400">{testimonial.metrics.insights}</p>p>
                                                                                                        <p className="text-sm text-white/50">More insights</p>p>
                                                                                    </div>div>
                                                              </div>div>
                                          )}
                          </motion.div>motion.div>
                        ))}
                                  </div>div>
                        </div>div>
                </section>section>
          
            {/* Pricing Section */}
                <section id="pricing" className="relative z-10 py-24 px-6">
                        <div className="max-w-7xl mx-auto">
                                  <div className="text-center mb-16">
                                              <span className="inline-block px-4 py-2 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-400 text-sm font-medium mb-4">PRICING</span>span>
                                              <h2 className="text-4xl lg:text-5xl font-bold mb-6">
                                                            Simple, <span className="bg-gradient-to-r from-violet-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">transparent pricing</span>span>
                                              </h2>h2>
                                              <p className="text-white/60 max-w-2xl mx-auto">
                                                            Choose the plan that fits your needs. All plans include a 14-day free trial.
                                              </p>
                                  </div>div>
                        
                                  <div className="grid md:grid-cols-3 gap-8">
                                    {pricingPlans.map((plan, i) => (
                          <motion.div
                                            key={i}
                                            className={`p-8 rounded-3xl ${plan.popular ? 'bg-gradient-to-b from-violet-500/20 to-transparent border-violet-500/30' : 'bg-white/[0.02] border-white/10'} border relative`}
                                            initial={{ opacity: 0, y: 20 }}
                                            whileInView={{ opacity: 1, y: 0 }}
                                            viewport={{ once: true }}
                                            transition={{ delay: i * 0.1 }}
                                          >
                            {plan.popular && (
                                                              <span className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 bg-violet-500 rounded-full text-xs font-semibold">Most Popular</span>span>
                                          )}
                                          <h3 className="text-xl font-semibold mb-2">{plan.name}</h3>h3>
                                          <div className="mb-4">
                                                            <span className="text-4xl font-bold">{plan.price}</span>span>
                                                            <span className="text-white/50">{plan.period}</span>span>
                                          </div>div>
                                          <p className="text-white/60 mb-6">{plan.desc}</p>p>
                                          <ul className="space-y-3 mb-8">
                                            {plan.features.map((feature, j) => (
                                                                <li key={j} className="flex items-center gap-3 text-white/70">
                                                                                      <span className="text-emerald-400">✓</span>span>
                                                                  {feature}
                                                                </li>li>
                                                              ))}
                                          </ul>ul>
                                          <button className={`w-full py-3 rounded-xl font-semibold transition-all ${plan.popular ? 'bg-gradient-to-r from-violet-600 to-purple-600 hover:shadow-lg hover:shadow-violet-500/25' : 'border border-white/20 hover:bg-white/5'}`}>
                                            {plan.cta}
                                          </button>button>
                          </motion.div>motion.div>
                        ))}
                                  </div>div>
                        </div>div>
                </section>section>
          
            {/* CTA Section */}
                <section className="relative z-10 py-24 px-6">
                        <div className="max-w-4xl mx-auto text-center p-12 rounded-3xl bg-gradient-to-br from-violet-500/20 via-pink-500/10 to-transparent border border-white/10">
                                  <h2 className="text-4xl lg:text-5xl font-bold mb-6">
                                              Ready to transform<br />your workflow?
                                  </h2>h2>
                                  <p className="text-white/60 mb-8 max-w-xl mx-auto">
                                              Join thousands of teams already using Luciq AI to work smarter, not harder.
                                  </p>p>
                                  <div className="flex flex-col sm:flex-row gap-4 justify-center">
                                              <button className="px-8 py-4 bg-gradient-to-r from-violet-600 to-purple-600 rounded-2xl font-semibold hover:shadow-xl hover:shadow-violet-500/25 hover:-translate-y-1 transition-all duration-300">
                                                            Start Free Trial →
                                              </button>button>
                                              <button className="px-8 py-4 rounded-2xl border border-white/20 font-medium hover:bg-white/5 transition-all">
                                                            Talk to Sales
                                              </button>button>
                                  </div>div>
                                  <p className="text-sm text-white/40 mt-6">No credit card required • 14-day free trial • Cancel anytime</p>p>
                        </div>div>
                </section>section>
          
            {/* Footer */}
                <footer className="relative z-10 border-t border-white/10 py-16 px-6">
                        <div className="max-w-7xl mx-auto">
                                  <div className="grid md:grid-cols-5 gap-12 mb-12">
                                              <div className="md:col-span-2">
                                                            <div className="flex items-center gap-2 mb-4">
                                                                            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center">
                                                                                              <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                                                                                                  <path d="M9 12l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" />
                                                                                                                  <circle cx="12" cy="12" r="10" />
                                                                                                </svg>svg>
                                                                            </div>div>
                                                                            <span className="text-xl font-bold">Luciq<span className="text-violet-400">AI</span>span></span>span>
                                                            </div>div>
                                                            <p className="text-white/50 max-w-xs">Your intelligent AI assistant for the digital age. Automate tasks, analyze data, and unlock insights at unprecedented speed.</p>p>
                                              </div>div>
                                    {[
            { title: 'PRODUCT', links: ['Features', 'Pricing', 'Integrations', 'Changelog', 'Roadmap'] },
            { title: 'COMPANY', links: ['About', 'Blog', 'Careers', 'Press'] },
            { title: 'RESOURCES', links: ['Documentation', 'API Reference', 'Guides', 'Community'] },
                        ].map((col, i) => (
                                        <div key={i}>
                                                        <h4 className="font-semibold text-white/70 text-sm mb-4">{col.title}</h4>h4>
                                                        <ul className="space-y-2">
                                                          {col.links.map((link, j) => (
                                                              <li key={j}><a href="#" className="text-white/50 hover:text-white text-sm transition-colors">{link}</a>a></li>li>
                                                            ))}
                                                        </ul>ul>
                                        </div>div>
                                      ))}
                                  </div>div>
                                  <div className="pt-8 border-t border-white/10 flex flex-col md:flex-row justify-between items-center gap-4">
                                              <p className="text-white/40 text-sm">© 2026 Luciq AI. All rights reserved.</p>p>
                                              <div className="flex items-center gap-6">
                                                            <span className="text-white/40 text-sm">🌐 English</span>span>
                                                            <span className="text-white/40 text-sm flex items-center gap-2">
                                                                            <span className="w-2 h-2 rounded-full bg-emerald-400" />
                                                                            Status: All systems operational
                                                            </span>span>
                                              </div>div>
                                  </div>div>
                        </div>div>
                </footer>footer>
          </div>div>
        );
}</div>
