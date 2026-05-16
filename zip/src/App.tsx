import React, { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  ChevronLeft,
  ChevronRight,
  Monitor,
  ShieldCheck,
  Network,
  Activity,
  Target,
  AlertCircle,
  CheckCircle,
  Layers,
  Wrench,
  ArrowRight,
  Database,
  Lock,
  Zap,
} from "lucide-react";

const slides = [
  {
    id: "title",
    content: (
      <div className="flex-1 flex flex-col justify-center items-start max-w-4xl">
        <motion.div
          initial={{ scaleY: 0 }}
          animate={{ scaleY: 1 }}
          transition={{ duration: 0.5 }}
          className="w-2 h-32 bg-cyan-500 mb-8 origin-top"
        ></motion.div>
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-6xl md:text-8xl font-bold text-white mb-4 tracking-tight"
        >
          ORBIT
        </motion.h1>
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-3xl md:text-4xl text-cyan-400 mb-12 font-light"
        >
          Strategic Integrity System
        </motion.h2>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="space-y-2 text-gray-400 text-xl"
        >
          <p>Subject: Project Management</p>
          <p>Group Members: Aditya Sadhu, Rohit Pandit, Khushi, Vanshita, Shrawan</p>
          <p>Guide Name: Mrs Rani Devi (Rani mam)</p>
        </motion.div>
      </div>
    ),
  },
  {
    id: "intro",
    content: (
      <div className="flex-1 flex flex-col justify-center max-w-5xl mx-auto w-full">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-16 border-b border-gray-800 pb-4 flex items-center gap-4">
          <Monitor className="w-10 h-10 text-cyan-500" />
          Introduction
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {[
            {
              title: "Project Management",
              desc: "ORBIT is a comprehensive project management system.",
              icon: <Layers />,
            },
            {
              title: "Task Tracking",
              desc: "Tracks tasks and activities across the organization.",
              icon: <Activity />,
            },
            {
              title: "Transparency",
              desc: "Improves transparency and accountability.",
              icon: <ShieldCheck />,
            },
            {
              title: "Real-time Insights",
              desc: "Provides real-time insights into project health.",
              icon: <Zap />,
            },
          ].map((item, i) => (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 + 0.2 }}
              key={i}
              className="bg-gray-900/50 border border-gray-800 p-8 rounded-xl flex items-start gap-6 hover:border-cyan-500/50 transition-colors"
            >
              <div className="p-3 bg-cyan-500/10 text-cyan-400 rounded-lg">
                {item.icon}
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white mb-2">
                  {item.title}
                </h3>
                <p className="text-gray-400 leading-relaxed">{item.desc}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    ),
  },
  {
    id: "problem",
    content: (
      <div className="flex-1 flex flex-col justify-center max-w-5xl mx-auto w-full">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-16 border-b border-gray-800 pb-4 flex items-center gap-4">
          <AlertCircle className="w-10 h-10 text-red-500" />
          Problem Statement
        </h2>
        <div className="space-y-6">
          {[
            "Lack of transparency in task execution",
            "Poor coordination among team members",
            "No real-time tracking of project progress",
            "Difficulty monitoring overall performance",
          ].map((text, i) => (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 + 0.2 }}
              key={i}
              className="flex items-center gap-6 bg-red-500/5 border border-red-500/10 p-6 rounded-lg"
            >
              <div className="w-3 h-3 rounded-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]" />
              <p className="text-2xl text-gray-300">{text}</p>
            </motion.div>
          ))}
        </div>
      </div>
    ),
  },
  {
    id: "objectives",
    content: (
      <div className="flex-1 flex flex-col justify-center max-w-5xl mx-auto w-full">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-16 border-b border-gray-800 pb-4 flex items-center gap-4">
          <Target className="w-10 h-10 text-green-500" />
          Objectives
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[
            "Improve tracking",
            "Ensure accountability",
            "Provide real-time updates",
            "Enhance coordination",
          ].map((text, i) => (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.1 + 0.2 }}
              key={i}
              className="bg-gradient-to-br from-gray-900 to-gray-800 border border-gray-700 p-8 rounded-xl flex flex-col items-center justify-center text-center gap-4 hover:border-green-500/50 transition-colors"
            >
              <CheckCircle className="w-12 h-12 text-green-400" />
              <p className="text-2xl text-white font-medium">{text}</p>
            </motion.div>
          ))}
        </div>
      </div>
    ),
  },
  {
    id: "scope",
    content: (
      <div className="flex-1 flex flex-col justify-center max-w-5xl mx-auto w-full">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-16 border-b border-gray-800 pb-4 flex items-center gap-4">
          <Layers className="w-10 h-10 text-purple-500" />
          Project Scope & Impact
        </h2>
        <div className="relative border-l-4 border-purple-500/30 ml-6 space-y-12 pb-8">
          {[
            {
              title: "Organizational Use",
              desc: "Designed to be used across various departments in organizations.",
            },
            {
              title: "Team & Task Management",
              desc: "Efficiently manages teams and assigns tasks dynamically.",
            },
            {
              title: "Role-based Access",
              desc: "Helps admins and auditors with specific, tailored workspaces.",
            },
            {
              title: "Scalability",
              desc: "A highly scalable system built to grow with the organization.",
            },
          ].map((item, i) => (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 + 0.2 }}
              key={i}
              className="relative pl-10"
            >
              <div className="absolute -left-[22px] top-1 w-10 h-10 bg-gray-900 border-4 border-purple-500 rounded-full flex items-center justify-center">
                <div className="w-3 h-3 bg-purple-400 rounded-full" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">
                {item.title}
              </h3>
              <p className="text-xl text-gray-400">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    ),
  },
  {
    id: "deliverables",
    content: (
      <div className="flex-1 flex flex-col justify-center max-w-5xl mx-auto w-full">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-16 border-b border-gray-800 pb-4 flex items-center gap-4">
          <Database className="w-10 h-10 text-emerald-500" />
          Project Deliverables
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[
            {
              title: "Admin Workspace",
              desc: "Dashboard for task assignment and workflow monitoring.",
            },
            {
              title: "Auditor Workspace",
              desc: "Forensic view for tracking system mutations and changes.",
            },
            {
              title: "Integrator Workspace",
              desc: "API connection manager and webhook configuration.",
            },
            {
              title: "Final Project Report",
              desc: "Comprehensive documentation of the system architecture.",
            },
          ].map((item, i) => (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 + 0.2 }}
              key={i}
              className="bg-emerald-500/5 border border-emerald-500/20 p-8 rounded-xl hover:bg-emerald-500/10 transition-colors"
            >
              <h3 className="text-2xl font-bold text-emerald-400 mb-3">
                {item.title}
              </h3>
              <p className="text-gray-400 text-lg">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    ),
  },
  {
    id: "planning",
    content: (
      <div className="flex-1 flex flex-col justify-center max-w-6xl mx-auto w-full">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-16 border-b border-gray-800 pb-4 flex items-center gap-4">
          <Activity className="w-10 h-10 text-orange-500" />
          Execution Plan & Timeline
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            {
              phase: "Phase 1",
              week: "Week 2",
              title: "Synopsis Submission",
              desc: "Problem selection, objectives, and initial planning.",
            },
            {
              phase: "Phase 2",
              week: "Week 6",
              title: "Progress Report-I",
              desc: "Requirement analysis, design, and initial development.",
            },
            {
              phase: "Phase 3",
              week: "Week 10",
              title: "Progress Report-II",
              desc: "Significant advancements, testing, and milestone tracking.",
            },
            {
              phase: "Phase 4",
              week: "Week 12-13",
              title: "Final Report & Sync",
              desc: "Preliminary draft, final copy, and group presentation.",
            },
          ].map((step, i) => (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 + 0.2 }}
              key={i}
              className="bg-gray-900 border border-gray-700 rounded-xl p-6 relative overflow-hidden group hover:border-orange-500/50 transition-colors"
            >
              <div className="absolute top-0 left-0 w-full h-1 bg-orange-500/50" />
              <div className="text-orange-400 font-mono text-sm mb-1">
                {step.week}
              </div>
              <h3 className="text-xl font-bold text-white mb-3">
                {step.title}
              </h3>
              <p className="text-gray-400 text-sm">{step.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    ),
  },
  {
    id: "tools",
    content: (
      <div className="flex-1 flex flex-col justify-center max-w-5xl mx-auto w-full">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-16 border-b border-gray-800 pb-4 flex items-center gap-4">
          <Wrench className="w-10 h-10 text-blue-500" />
          Tools & Technologies
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {[
            {
              title: "Dashboard Interface",
              icon: <Monitor className="w-8 h-8" />,
            },
            { title: "API Integration", icon: <Network className="w-8 h-8" /> },
            { title: "Data Tracking", icon: <Database className="w-8 h-8" /> },
            {
              title: "Real-time Monitoring",
              icon: <Activity className="w-8 h-8" />,
            },
          ].map((item, i) => (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.1 + 0.2 }}
              key={i}
              className="bg-gray-900/80 border border-gray-700 p-8 rounded-2xl flex items-center gap-6 hover:bg-gray-800 transition-colors"
            >
              <div className="p-4 bg-blue-500/10 text-blue-400 rounded-xl">
                {item.icon}
              </div>
              <h3 className="text-2xl font-semibold text-gray-200">
                {item.title}
              </h3>
            </motion.div>
          ))}
        </div>
      </div>
    ),
  },
  {
    id: "overview",
    content: (
      <div className="flex-1 flex flex-col justify-center max-w-5xl mx-auto w-full text-center">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-16 flex items-center justify-center gap-4">
          <Network className="w-12 h-12 text-cyan-500" />
          System Overview
        </h2>
        <div className="flex flex-col md:flex-row justify-center items-center gap-8 md:gap-16">
          {[
            {
              title: "Admin Workspace",
              icon: <Lock className="w-12 h-12 mb-4 text-cyan-400" />,
            },
            {
              title: "Auditor Workspace",
              icon: <ShieldCheck className="w-12 h-12 mb-4 text-purple-400" />,
            },
            {
              title: "Integrator Workspace",
              icon: <Network className="w-12 h-12 mb-4 text-blue-400" />,
            },
          ].map((item, i) => (
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.2 + 0.2 }}
              key={i}
              className="flex flex-col items-center bg-gray-900/50 border border-gray-800 p-10 rounded-2xl w-full md:w-1/3 hover:border-cyan-500/30 transition-colors"
            >
              {item.icon}
              <h3 className="text-2xl font-bold text-white">{item.title}</h3>
            </motion.div>
          ))}
        </div>
      </div>
    ),
  },
  {
    id: "admin",
    content: (
      <div className="flex-1 flex flex-col max-w-7xl mx-auto w-full h-full justify-center">
        <div className="flex flex-col md:flex-row gap-12 items-center">
          <div className="w-full md:w-1/3">
            <h2 className="text-4xl font-bold text-cyan-400 mb-6 uppercase tracking-wider border-b-2 border-cyan-500/30 pb-4">
              Admin Workspace
            </h2>
            <ul className="space-y-6">
              {[
                "Manages tasks",
                "Monitors progress",
                "Provides dashboard",
                "Ensures workflow",
              ].map((text, i) => (
                <motion.li
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 + 0.2 }}
                  key={i}
                  className="flex items-center gap-4 text-xl text-gray-300"
                >
                  <div className="w-2 h-2 bg-cyan-500 rounded-full" />
                  {text}
                </motion.li>
              ))}
            </ul>
            <p className="mt-12 text-gray-500 italic">
              Supervisor Dashboard: Real-time task management and project health
              metrics.
            </p>
          </div>
          <div className="w-full md:w-2/3">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4 }}
              className="bg-[#0f0f13] rounded-xl border border-cyan-500/30 shadow-[0_0_30px_rgba(6,182,212,0.15)] overflow-hidden"
            >
              <div className="p-6 border-b border-gray-800">
                <div className="inline-block px-3 py-1 bg-purple-500/10 text-purple-400 text-xs font-semibold rounded mb-4">
                  TASK MANAGEMENT
                </div>
                <h3 className="text-2xl font-bold text-white mb-1">
                  Active Assignments
                </h3>
                <p className="text-sm text-gray-400">
                  Manage and track project tasks across all roles.
                </p>
              </div>
              <div className="p-6 space-y-6">
                <div>
                  <h4 className="text-sm font-semibold text-white mb-3">
                    Create New Task
                  </h4>
                  <div className="space-y-3">
                    <div>
                      <label className="text-xs text-gray-500 mb-1 block">
                        Task Title
                      </label>
                      <div className="w-full h-10 bg-[#16161a] rounded border border-gray-800 flex items-center px-3 text-sm text-gray-600">
                        e.g. Update user documentation
                      </div>
                    </div>
                    <div>
                      <label className="text-xs text-gray-500 mb-1 block">
                        Task Details
                      </label>
                      <div className="w-full h-10 bg-[#16161a] rounded border border-gray-800 flex items-center px-3 text-sm text-gray-600">
                        Describe the requirements...
                      </div>
                    </div>
                    <button className="px-4 py-2 bg-purple-600/20 text-purple-400 text-xs font-bold rounded border border-purple-500/30 hover:bg-purple-600/30 transition-colors">
                      DEPLOY TASK
                    </button>
                  </div>
                </div>
                <div className="rounded border border-gray-800 overflow-hidden">
                  <div className="bg-[#16161a] grid grid-cols-4 p-3 text-xs font-bold text-gray-500 uppercase">
                    <div>ID</div>
                    <div>DESCRIPTION</div>
                    <div>STATUS</div>
                    <div>ACTION</div>
                  </div>
                  <div className="p-8 text-center text-sm text-gray-600 bg-[#0f0f13]">
                    No tasks found.
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    ),
  },
  {
    id: "auditor",
    content: (
      <div className="flex-1 flex flex-col max-w-7xl mx-auto w-full h-full justify-center">
        <div className="flex flex-col md:flex-row gap-12 items-center">
          <div className="w-full md:w-1/3">
            <h2 className="text-4xl font-bold text-cyan-400 mb-6 uppercase tracking-wider border-b-2 border-cyan-500/30 pb-4">
              Auditor Workspace
            </h2>
            <ul className="space-y-6">
              {[
                "Tracks activities",
                "Records changes",
                "Ensures transparency",
                "Helps auditing",
              ].map((text, i) => (
                <motion.li
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 + 0.2 }}
                  key={i}
                  className="flex items-center gap-4 text-xl text-gray-300"
                >
                  <div className="w-2 h-2 bg-cyan-500 rounded-full" />
                  {text}
                </motion.li>
              ))}
            </ul>
            <p className="mt-12 text-gray-500 italic">
              Auditor Forensic View: Every system mutation recorded with
              precision timestamps.
            </p>
          </div>
          <div className="w-full md:w-2/3">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4 }}
              className="bg-[#0f0f13] rounded-xl border border-cyan-500/30 shadow-[0_0_30px_rgba(6,182,212,0.15)] overflow-hidden p-8"
            >
              <div className="flex justify-between items-center mb-12">
                <button className="text-xs text-red-400 border border-red-500/30 px-3 py-1 rounded hover:bg-red-500/10">
                  Log Out
                </button>
                <span className="text-xs text-gray-500">Team View</span>
              </div>
              <div className="text-center mb-12">
                <h3 className="text-3xl font-bold text-purple-400 mb-2">
                  Orbit Project Manager
                </h3>
                <p className="text-xs text-gray-500">
                  Welcome, auditor_test | Access Level: PRID_2
                </p>
              </div>
              <div className="bg-red-500/5 border border-red-500/20 rounded p-4 text-center text-xs text-red-400 mb-8">
                Registration successful. PRID linked to main orchestrator.
              </div>
              <div className="bg-[#16161a] border border-gray-800 rounded p-6 mb-8">
                <div className="flex justify-between text-xs font-bold text-white mb-4">
                  <span>Project Completion</span>
                  <span>0%</span>
                </div>
                <div className="w-full h-2 bg-gray-800 rounded-full overflow-hidden">
                  <div className="w-0 h-full bg-white"></div>
                </div>
              </div>
              <div className="bg-[#16161a] border border-gray-800 rounded p-6 opacity-50">
                <div className="inline-block px-3 py-1 bg-purple-500/10 text-purple-400 text-xs font-semibold rounded mb-4">
                  TASK MANAGEMENT
                </div>
                <h4 className="text-lg font-bold text-white mb-1">
                  Active Assignments
                </h4>
                <p className="text-xs text-gray-500">
                  Manage and track project tasks across all roles.
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    ),
  },
  {
    id: "integrator",
    content: (
      <div className="flex-1 flex flex-col max-w-7xl mx-auto w-full h-full justify-center">
        <div className="flex flex-col md:flex-row gap-12 items-center">
          <div className="w-full md:w-1/3">
            <h2 className="text-4xl font-bold text-cyan-400 mb-6 uppercase tracking-wider border-b-2 border-cyan-500/30 pb-4">
              Integrator Workspace
            </h2>
            <ul className="space-y-6">
              {[
                "Connects APIs",
                "Manages data exchange",
                "Ensures synchronization",
                "Supports integration",
              ].map((text, i) => (
                <motion.li
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 + 0.2 }}
                  key={i}
                  className="flex items-center gap-4 text-xl text-gray-300"
                >
                  <div className="w-2 h-2 bg-cyan-500 rounded-full" />
                  {text}
                </motion.li>
              ))}
            </ul>
            <p className="mt-12 text-gray-500 italic">
              Integrator Workspace: Managing real-time external API connections.
            </p>
          </div>
          <div className="w-full md:w-2/3">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4 }}
              className="bg-[#0f0f13] rounded-xl border border-cyan-500/30 shadow-[0_0_30px_rgba(6,182,212,0.15)] overflow-hidden p-8"
            >
              <div className="flex justify-between items-center mb-12">
                <button className="text-xs text-red-400 border border-red-500/30 px-3 py-1 rounded hover:bg-red-500/10">
                  Log Out
                </button>
                <span className="text-xs text-gray-500">Team View</span>
              </div>
              <div className="text-center mb-12">
                <h3 className="text-3xl font-bold text-purple-400 mb-2">
                  Orbit Project Manager
                </h3>
                <p className="text-xs text-gray-500">
                  Welcome, integrator_v3 | Access Level: PRID_4
                </p>
              </div>
              <div className="bg-red-500/5 border border-red-500/20 rounded p-4 text-center text-xs text-red-400 mb-8">
                Registration successful. PRID linked to main orchestrator.
              </div>
              <div className="bg-[#16161a] border border-gray-800 rounded p-6 mb-8">
                <div className="flex justify-between text-xs font-bold text-white mb-4">
                  <span>Project Completion</span>
                  <span>0%</span>
                </div>
                <div className="w-full h-2 bg-gray-800 rounded-full overflow-hidden">
                  <div className="w-0 h-full bg-white"></div>
                </div>
              </div>
              <div className="bg-[#16161a] border border-gray-800 rounded p-6">
                <div className="inline-block px-3 py-1 bg-purple-500/10 text-purple-400 text-xs font-semibold rounded mb-4">
                  INTEGRATIONS
                </div>
                <h4 className="text-lg font-bold text-white mb-1">Webhooks</h4>
                <p className="text-xs text-gray-500 mb-4">
                  Link external services to your workspace.
                </p>
                <div className="space-y-3">
                  <div className="w-full h-10 bg-[#0f0f13] rounded border border-gray-800 flex items-center px-3 text-sm text-gray-600">
                    https://api.service.com/hook
                  </div>
                  <button className="w-full py-2 bg-purple-600/10 text-purple-400 text-xs font-bold rounded border border-purple-500/30 hover:bg-purple-600/20 transition-colors uppercase tracking-wider">
                    Add Webhook
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    ),
  },
  {
    id: "conclusion",
    content: (
      <div className="flex-1 flex flex-col justify-center items-center max-w-4xl mx-auto w-full text-center">
        <h2 className="text-5xl md:text-7xl font-bold text-cyan-400 mb-8 tracking-tight">
          READY FOR SYNC
        </h2>
        <p className="text-2xl text-gray-400 mb-16">
          Final Project Demonstration
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full mt-8">
          {[
            {
              title: "Improves Transparency",
              icon: <ShieldCheck className="w-8 h-8 text-green-400" />,
            },
            {
              title: "Better Decisions",
              icon: <Target className="w-8 h-8 text-blue-400" />,
            },
            {
              title: "Future: AI & Mobile",
              icon: <Zap className="w-8 h-8 text-purple-400" />,
            },
          ].map((item, i) => (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.2 + 0.4 }}
              key={i}
              className="bg-gray-900/50 border border-gray-800 p-6 rounded-xl flex flex-col items-center gap-4"
            >
              {item.icon}
              <h3 className="text-lg font-semibold text-gray-200">
                {item.title}
              </h3>
            </motion.div>
          ))}
        </div>
      </div>
    ),
  },
  {
    id: "qna",
    content: (
      <div className="flex-1 flex flex-col justify-center items-center max-w-4xl mx-auto w-full text-center">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="w-24 h-24 bg-cyan-500/20 rounded-full flex items-center justify-center mb-8"
        >
          <AlertCircle className="w-12 h-12 text-cyan-400" />
        </motion.div>
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-5xl md:text-7xl font-bold text-white mb-6 tracking-tight"
        >
          Questions & Feedback
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-2xl text-gray-400 max-w-2xl"
        >
          Thank you for your time. We are now open to any questions, feedback,
          or suggestions from the audience and panel.
        </motion.p>
      </div>
    ),
  },
];

export default function App() {
  return (
    <div className="w-full min-h-screen bg-[#0B1120] bg-grid-pattern font-sans flex flex-col">
      {slides.map((slide, index) => (
        <div
          key={slide.id}
          data-slide-id={slide.id}
          className="w-full min-h-screen flex flex-col p-8 md:p-16 lg:p-24 relative border-b border-gray-800/30 break-after-page"
          style={{ pageBreakAfter: "always" }}
        >
          <div className="absolute bottom-8 right-8 text-gray-500 font-mono text-sm bg-gray-900/50 px-3 py-1 rounded-full backdrop-blur-sm border border-gray-800">
            {index + 1} / {slides.length}
          </div>
          {slide.content}
        </div>
      ))}
    </div>
  );
}
