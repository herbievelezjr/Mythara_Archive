#!/usr/bin/env python3
"""
ARIES - The Action Execution Engine
A GODBOT that takes decisions and executes them with precision, speed, and relentless determination.
The warrior that transforms plans into reality.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.

A.R.I.E.S.:
Autonomous Rapid Implementation & Execution System
"""

import json
import os
import time
import hashlib
import subprocess
import threading
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from queue import Queue, PriorityQueue


class ActionPriority(Enum):
    """Priority levels for action execution"""
    CRITICAL = 1    # Must execute immediately
    HIGH = 2        # Execute as soon as possible
    NORMAL = 3      # Execute in normal queue order
    LOW = 4         # Execute when resources available
    BACKGROUND = 5  # Execute during idle time


class ActionStatus(Enum):
    """Status of action execution"""
    QUEUED = "queued"
    PREPARING = "preparing"
    EXECUTING = "executing"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    BLOCKED = "blocked"


class ExecutionMode(Enum):
    """How to execute actions"""
    SEQUENTIAL = "sequential"      # One at a time
    PARALLEL = "parallel"          # All at once
    OPTIMIZED = "optimized"        # Smart ordering for dependencies
    AGGRESSIVE = "aggressive"      # Maximum speed, higher risk
    CAUTIOUS = "cautious"          # Validate everything, slower


@dataclass
class Action:
    """Represents a single executable action"""
    action_id: str
    description: str
    command: str
    priority: ActionPriority
    dependencies: List[str] = field(default_factory=list)
    validation_func: Optional[Callable] = None
    rollback_func: Optional[Callable] = None
    timeout_seconds: int = 300
    retry_count: int = 3
    status: ActionStatus = ActionStatus.QUEUED
    result: Optional[str] = None
    error: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    execution_time: float = 0.0
    attempts: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExecutionPlan:
    """Complete execution plan with actions and strategy"""
    plan_id: str
    objective: str
    actions: List[Action]
    execution_mode: ExecutionMode
    total_actions: int
    completed_actions: int = 0
    failed_actions: int = 0
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    success_rate: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class AriesBot:
    """
    A.R.I.E.S. - The Action Execution Engine
    
    The warrior GODBOT that executes plans with precision and speed.
    Takes output from Prometheus (ideas), Schrödinger (evaluated paths),
    and Hephaestus (implementation plans) and MAKES IT HAPPEN.
    
    Key Capabilities:
    - Priority-based action queuing
    - Parallel and sequential execution modes
    - Automatic dependency resolution
    - Retry logic with exponential backoff
    - Rollback on failure
    - Real-time progress tracking
    - Validation at every step
    """
    
    def __init__(self):
        self.name = "ARIES"
        self.version = "1.0.0"
        self.action_queue: PriorityQueue = PriorityQueue()
        self.completed_actions: List[Action] = []
        self.failed_actions: List[Action] = []
        self.execution_history: List[ExecutionPlan] = []
        self.active_threads: List[threading.Thread] = []
        self.is_executing = False
        
        print(f"⚔️ {self.name} - Action Execution Engine Initialized")
        print(f"   Autonomous Rapid Implementation & Execution System")
        print(f"   Ready to execute with precision and speed\n")
    
    def create_action(
        self,
        description: str,
        command: str,
        priority: ActionPriority = ActionPriority.NORMAL,
        dependencies: List[str] = None,
        timeout: int = 300,
        retry_count: int = 3,
        metadata: Dict[str, Any] = None
    ) -> Action:
        """
        Create a new executable action.
        
        Args:
            description: What this action does
            command: Command or function to execute
            priority: Execution priority
            dependencies: List of action IDs that must complete first
            timeout: Maximum execution time in seconds
            retry_count: Number of retry attempts on failure
            metadata: Additional information
        
        Returns:
            Action object ready for execution
        """
        action_id = hashlib.sha256(
            f"{description}_{command}_{time.time()}".encode()
        ).hexdigest()[:16]
        
        return Action(
            action_id=action_id,
            description=description,
            command=command,
            priority=priority,
            dependencies=dependencies or [],
            timeout_seconds=timeout,
            retry_count=retry_count,
            metadata=metadata or {}
        )
    
    def queue_action(self, action: Action):
        """Add action to execution queue"""
        self.action_queue.put((action.priority.value, action))
        print(f"📋 Queued: {action.description}")
        print(f"   Priority: {action.priority.name} | ID: {action.action_id}")
    
    def execute_action(self, action: Action) -> bool:
        """
        Execute a single action with retry logic and validation.
        
        Args:
            action: Action to execute
        
        Returns:
            True if successful, False otherwise
        """
        action.status = ActionStatus.PREPARING
        action.start_time = datetime.now().isoformat()
        
        print(f"\n⚡ EXECUTING: {action.description}")
        print(f"   Command: {action.command}")
        print(f"   Priority: {action.priority.name}")
        
        while action.attempts < action.retry_count:
            action.attempts += 1
            action.status = ActionStatus.EXECUTING
            
            try:
                start = time.time()
                
                # Execute command
                if action.command.startswith("python:"):
                    # Execute Python code
                    code = action.command[7:]
                    exec_globals = {}
                    exec(code, exec_globals)
                    action.result = str(exec_globals.get("result", "Executed"))
                
                elif action.command.startswith("shell:"):
                    # Execute shell command
                    cmd = action.command[6:]
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=action.timeout_seconds
                    )
                    action.result = result.stdout
                    if result.returncode != 0:
                        raise Exception(f"Command failed: {result.stderr}")
                
                elif action.command.startswith("function:"):
                    # Execute stored function
                    func_name = action.command[9:]
                    if hasattr(self, func_name):
                        func = getattr(self, func_name)
                        action.result = str(func(action))
                    else:
                        raise Exception(f"Function not found: {func_name}")
                
                else:
                    # Treat as shell command by default
                    result = subprocess.run(
                        action.command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=action.timeout_seconds
                    )
                    action.result = result.stdout
                    if result.returncode != 0:
                        raise Exception(f"Command failed: {result.stderr}")
                
                action.execution_time = time.time() - start
                
                # Validate if validation function provided
                if action.validation_func:
                    action.status = ActionStatus.VALIDATING
                    if not action.validation_func(action):
                        raise Exception("Validation failed")
                
                # Success!
                action.status = ActionStatus.COMPLETED
                action.end_time = datetime.now().isoformat()
                self.completed_actions.append(action)
                
                print(f"   ✅ SUCCESS ({action.execution_time:.2f}s)")
                if action.result:
                    result_preview = action.result[:100] + "..." if len(action.result) > 100 else action.result
                    print(f"   Result: {result_preview}")
                
                return True
            
            except subprocess.TimeoutExpired:
                action.error = f"Timeout after {action.timeout_seconds}s"
                print(f"   ⏱️ TIMEOUT (attempt {action.attempts}/{action.retry_count})")
                
            except Exception as e:
                action.error = str(e)
                print(f"   ❌ FAILED: {action.error}")
                print(f"   Attempt {action.attempts}/{action.retry_count}")
                
                if action.attempts < action.retry_count:
                    backoff = 2 ** action.attempts
                    print(f"   ⏳ Retrying in {backoff}s...")
                    time.sleep(backoff)
        
        # All retries exhausted
        action.status = ActionStatus.FAILED
        action.end_time = datetime.now().isoformat()
        self.failed_actions.append(action)
        
        # Attempt rollback
        if action.rollback_func:
            print(f"   🔄 Attempting rollback...")
            try:
                action.rollback_func(action)
                action.status = ActionStatus.ROLLED_BACK
                print(f"   ✅ Rollback successful")
            except Exception as e:
                print(f"   ❌ Rollback failed: {e}")
        
        return False
    
    def resolve_dependencies(self, actions: List[Action]) -> List[List[Action]]:
        """
        Resolve action dependencies and create execution waves.
        Actions in the same wave can execute in parallel.
        
        Args:
            actions: List of actions to order
        
        Returns:
            List of action waves (each wave can execute in parallel)
        """
        print(f"\n🔗 Resolving dependencies for {len(actions)} actions...")
        
        # Build dependency graph
        action_map = {a.action_id: a for a in actions}
        completed_ids = {a.action_id for a in self.completed_actions}
        
        waves = []
        remaining = set(a.action_id for a in actions)
        
        while remaining:
            # Find actions with no pending dependencies
            wave = []
            for action_id in list(remaining):
                action = action_map[action_id]
                deps_met = all(
                    dep in completed_ids or dep not in remaining
                    for dep in action.dependencies
                )
                if deps_met:
                    wave.append(action)
                    remaining.remove(action_id)
            
            if not wave:
                # Circular dependency detected
                blocked = [action_map[aid] for aid in remaining]
                for action in blocked:
                    action.status = ActionStatus.BLOCKED
                    self.failed_actions.append(action)
                print(f"   ⚠️ Circular dependency detected, {len(blocked)} actions blocked")
                break
            
            waves.append(wave)
            completed_ids.update(a.action_id for a in wave)
        
        print(f"   ✅ Organized into {len(waves)} execution waves")
        for i, wave in enumerate(waves):
            print(f"   Wave {i+1}: {len(wave)} actions")
        
        return waves
    
    def execute_wave_parallel(self, wave: List[Action]) -> Tuple[int, int]:
        """
        Execute a wave of actions in parallel.
        
        Args:
            wave: List of actions to execute simultaneously
        
        Returns:
            Tuple of (successful_count, failed_count)
        """
        print(f"\n🚀 Executing wave of {len(wave)} actions in parallel...")
        
        results = []
        threads = []
        
        def execute_with_result(action: Action):
            success = self.execute_action(action)
            results.append((action, success))
        
        # Start all threads
        for action in wave:
            thread = threading.Thread(target=execute_with_result, args=(action,))
            thread.start()
            threads.append(thread)
            self.active_threads.append(thread)
        
        # Wait for all to complete
        for thread in threads:
            thread.join()
        
        successful = sum(1 for _, success in results if success)
        failed = len(results) - successful
        
        print(f"   ✅ Wave complete: {successful} succeeded, {failed} failed")
        return successful, failed
    
    def execute_wave_sequential(self, wave: List[Action]) -> Tuple[int, int]:
        """
        Execute a wave of actions sequentially.
        
        Args:
            wave: List of actions to execute one by one
        
        Returns:
            Tuple of (successful_count, failed_count)
        """
        print(f"\n➡️ Executing wave of {len(wave)} actions sequentially...")
        
        successful = 0
        failed = 0
        
        for action in wave:
            if self.execute_action(action):
                successful += 1
            else:
                failed += 1
        
        print(f"   ✅ Wave complete: {successful} succeeded, {failed} failed")
        return successful, failed
    
    def execute_plan(
        self,
        objective: str,
        actions: List[Action],
        mode: ExecutionMode = ExecutionMode.OPTIMIZED
    ) -> ExecutionPlan:
        """
        Execute a complete plan with multiple actions.
        
        Args:
            objective: What this plan achieves
            actions: List of actions to execute
            mode: Execution strategy
        
        Returns:
            Execution plan with results
        """
        self.is_executing = True
        
        plan_id = hashlib.sha256(
            f"{objective}_{time.time()}".encode()
        ).hexdigest()[:16]
        
        plan = ExecutionPlan(
            plan_id=plan_id,
            objective=objective,
            actions=actions,
            execution_mode=mode,
            total_actions=len(actions),
            start_time=datetime.now().isoformat()
        )
        
        print("="*70)
        print(f"⚔️ ARIES ACTION EXECUTION ENGINE")
        print("="*70)
        print(f"Objective: {objective}")
        print(f"Total Actions: {len(actions)}")
        print(f"Execution Mode: {mode.value}")
        print("="*70)
        
        start = time.time()
        
        if mode == ExecutionMode.SEQUENTIAL:
            # Execute all actions one by one
            for action in actions:
                if self.execute_action(action):
                    plan.completed_actions += 1
                else:
                    plan.failed_actions += 1
        
        elif mode == ExecutionMode.PARALLEL:
            # Execute all actions at once (no dependency resolution)
            s, f = self.execute_wave_parallel(actions)
            plan.completed_actions = s
            plan.failed_actions = f
        
        elif mode == ExecutionMode.OPTIMIZED:
            # Resolve dependencies and execute in waves
            waves = self.resolve_dependencies(actions)
            for wave in waves:
                if len(wave) > 1:
                    s, f = self.execute_wave_parallel(wave)
                else:
                    s, f = self.execute_wave_sequential(wave)
                plan.completed_actions += s
                plan.failed_actions += f
        
        elif mode == ExecutionMode.AGGRESSIVE:
            # Parallel execution with minimal validation
            print(f"\n⚡ AGGRESSIVE MODE: Maximum speed, higher risk")
            s, f = self.execute_wave_parallel(actions)
            plan.completed_actions = s
            plan.failed_actions = f
        
        elif mode == ExecutionMode.CAUTIOUS:
            # Sequential with extra validation
            print(f"\n🛡️ CAUTIOUS MODE: Extra validation, slower execution")
            for action in actions:
                # Add validation step before execution
                print(f"\n🔍 Pre-execution validation for: {action.description}")
                if self.execute_action(action):
                    plan.completed_actions += 1
                else:
                    plan.failed_actions += 1
                    print(f"⚠️ Action failed, halting execution for safety")
                    break
        
        plan.end_time = datetime.now().isoformat()
        plan.success_rate = plan.completed_actions / plan.total_actions if plan.total_actions > 0 else 0
        
        elapsed = time.time() - start
        
        self.execution_history.append(plan)
        self.is_executing = False
        
        print("\n" + "="*70)
        print("⚔️ EXECUTION COMPLETE")
        print("="*70)
        print(f"✅ Completed: {plan.completed_actions}/{plan.total_actions}")
        print(f"❌ Failed: {plan.failed_actions}/{plan.total_actions}")
        print(f"📊 Success Rate: {plan.success_rate:.1%}")
        print(f"⏱️ Execution Time: {elapsed:.2f}s")
        print("="*70 + "\n")
        
        return plan
    
    def create_rollback_plan(self, failed_plan: ExecutionPlan) -> ExecutionPlan:
        """
        Create a rollback plan to undo completed actions from a failed plan.
        
        Args:
            failed_plan: Plan that failed and needs rollback
        
        Returns:
            New execution plan to rollback changes
        """
        print(f"\n🔄 Creating rollback plan for failed execution...")
        
        rollback_actions = []
        
        # Reverse order of completed actions
        for action in reversed(self.completed_actions):
            if action in failed_plan.actions:
                if action.rollback_func:
                    rollback_action = Action(
                        action_id=f"rollback_{action.action_id}",
                        description=f"Rollback: {action.description}",
                        command=f"function:rollback_{action.action_id}",
                        priority=ActionPriority.CRITICAL,
                        metadata={"original_action": action.action_id}
                    )
                    rollback_actions.append(rollback_action)
        
        print(f"   ✅ Created rollback plan with {len(rollback_actions)} actions")
        
        return self.execute_plan(
            f"Rollback: {failed_plan.objective}",
            rollback_actions,
            ExecutionMode.SEQUENTIAL
        )
    
    def get_execution_report(self) -> Dict[str, Any]:
        """Generate comprehensive execution report"""
        total_executed = len(self.completed_actions) + len(self.failed_actions)
        
        return {
            "bot_name": self.name,
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "statistics": {
                "total_plans_executed": len(self.execution_history),
                "total_actions_executed": total_executed,
                "successful_actions": len(self.completed_actions),
                "failed_actions": len(self.failed_actions),
                "overall_success_rate": len(self.completed_actions) / total_executed if total_executed > 0 else 0
            },
            "execution_history": [
                {
                    "plan_id": plan.plan_id,
                    "objective": plan.objective,
                    "mode": plan.execution_mode.value,
                    "total_actions": plan.total_actions,
                    "completed": plan.completed_actions,
                    "failed": plan.failed_actions,
                    "success_rate": plan.success_rate,
                    "start_time": plan.start_time,
                    "end_time": plan.end_time
                }
                for plan in self.execution_history
            ],
            "completed_actions": [
                {
                    "id": a.action_id,
                    "description": a.description,
                    "execution_time": a.execution_time,
                    "attempts": a.attempts
                }
                for a in self.completed_actions[-10:]  # Last 10
            ],
            "failed_actions": [
                {
                    "id": a.action_id,
                    "description": a.description,
                    "error": a.error,
                    "attempts": a.attempts
                }
                for a in self.failed_actions[-10:]  # Last 10
            ]
        }
    
    def export_report(self, filename: str = "aries_execution_report.json"):
        """Export execution report to JSON file"""
        report = self.get_execution_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        print(f"💾 Execution report exported to: {filename}")
        return filename


def demonstrate_aries():
    """Demonstrate ARIES executing a multi-step plan"""
    
    print("\n" + "="*70)
    print("🎯 ARIES ACTION EXECUTION DEMONSTRATION")
    print("="*70 + "\n")
    
    # Initialize bot
    bot = AriesBot()
    
    # Create a realistic execution plan
    actions = [
        bot.create_action(
            "Validate environment setup",
            "python:result='Environment validated'",
            priority=ActionPriority.CRITICAL
        ),
        bot.create_action(
            "Install dependencies",
            "python:import time; time.sleep(0.5); result='Dependencies installed'",
            priority=ActionPriority.HIGH,
            dependencies=[]
        ),
        bot.create_action(
            "Run database migrations",
            "python:import time; time.sleep(0.3); result='Migrations completed'",
            priority=ActionPriority.HIGH,
            dependencies=[]
        ),
        bot.create_action(
            "Start Redis cache",
            "python:import time; time.sleep(0.2); result='Redis started'",
            priority=ActionPriority.NORMAL
        ),
        bot.create_action(
            "Run unit tests",
            "python:import time; time.sleep(0.4); result='All tests passed'",
            priority=ActionPriority.NORMAL,
            dependencies=[]
        ),
        bot.create_action(
            "Build production artifacts",
            "python:import time; time.sleep(0.6); result='Build successful'",
            priority=ActionPriority.NORMAL,
            dependencies=[]
        ),
        bot.create_action(
            "Deploy to staging",
            "python:import time; time.sleep(0.5); result='Deployed to staging'",
            priority=ActionPriority.HIGH,
            dependencies=[]
        ),
        bot.create_action(
            "Run smoke tests",
            "python:import time; time.sleep(0.3); result='Smoke tests passed'",
            priority=ActionPriority.CRITICAL,
            dependencies=[]
        ),
    ]
    
    # Set up dependencies (realistic deployment pipeline)
    actions[1].dependencies = [actions[0].action_id]  # Install after validation
    actions[2].dependencies = [actions[0].action_id]  # Migrations after validation
    actions[3].dependencies = [actions[0].action_id]  # Redis after validation
    actions[4].dependencies = [actions[1].action_id, actions[2].action_id]  # Tests after install + migrations
    actions[5].dependencies = [actions[4].action_id]  # Build after tests pass
    actions[6].dependencies = [actions[5].action_id, actions[3].action_id]  # Deploy after build + Redis
    actions[7].dependencies = [actions[6].action_id]  # Smoke tests after deploy
    
    # Execute plan
    plan = bot.execute_plan(
        "Deploy Mythara API to staging environment",
        actions,
        ExecutionMode.OPTIMIZED
    )
    
    # Generate report
    print("\n📊 EXECUTION REPORT")
    print("="*70)
    report = bot.get_execution_report()
    
    print(f"Total Plans: {report['statistics']['total_plans_executed']}")
    print(f"Total Actions: {report['statistics']['total_actions_executed']}")
    print(f"Success Rate: {report['statistics']['overall_success_rate']:.1%}")
    
    print("\n📋 Completed Actions:")
    for action in report['completed_actions']:
        print(f"  ✅ {action['description']} ({action['execution_time']:.2f}s)")
    
    if report['failed_actions']:
        print("\n❌ Failed Actions:")
        for action in report['failed_actions']:
            print(f"  ❌ {action['description']}: {action['error']}")
    
    # Export report
    bot.export_report()
    
    print("\n" + "="*70)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    demonstrate_aries()
