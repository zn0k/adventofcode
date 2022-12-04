package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strings"
)

type Step struct {
	Name       string
	Completed  bool
	Conditions []string
	Queued     bool
}

func NewStep(name string) *Step {
	s := &Step{Name: name, Completed: false}
	s.Conditions = make([]string, 0)
	return s
}

type Steps struct {
	steps map[string]*Step
}

func (s *Steps) Add(name string) {
	_, ok := s.steps[name]
	if !ok {
		step := NewStep(name)
		s.steps[step.Name] = step
	}
}

func (s *Steps) AddCondition(name string, condition string) {
	step, ok := s.steps[name]
	if ok {
		step.Conditions = append(step.Conditions, condition)
	}
}

func (s *Steps) Complete(name string) {
	step, ok := s.steps[name]
	if ok {
		step.Completed = true
	}
}

func (s *Steps) Queue(name string) {
	step, ok := s.steps[name]
	if ok {
		step.Queued = true
	}
}

func (s *Steps) Get(name string) (*Step, bool) {
	step, ok := s.steps[name]
	if !ok {
		return &Step{}, false
	}
	return step, true
}

func (s *Steps) Next() (*Step, bool) {
	var candidates []string
	for _, step := range s.steps {
		if step.Completed || step.Queued {
			continue
		}
		if len(step.Conditions) == 0 {
			candidates = append(candidates, step.Name)
		} else {
			allCompleted := true
			for _, condition := range step.Conditions {
				step, _ := s.Get(condition)
				if !step.Completed {
					allCompleted = false
					break
				}
			}
			if allCompleted {
				candidates = append(candidates, step.Name)
			}
		}
	}

	sort.Strings(candidates)

	if len(candidates) > 0 {
		step, _ := s.Get(candidates[0])
		return step, true
	} else {
		return &Step{}, false
	}
}

func (s *Steps) Steps() map[string]*Step {
	return s.steps
}

func (s *Steps) Solve() string {
	sequence := ""
	for {
		step, more := s.Next()
		if !more {
			break
		}

		sequence += step.Name
		s.Complete(step.Name)
	}

	return sequence
}

func (s *Steps) SolveWorkers(count int, delay int) int {
	workers := NewWorkers(count, delay)
	ticks := -1
	for {
		done := workers.Tick()
		ticks += 1
		for _, work := range done {
			s.Complete(work.Step)
		}
		for {
			step, more := s.Next()
			if !more {
				break
			}
			result := workers.AddWork(Work{Step: step.Name})
			if !result {
				break
			}
			s.Queue(step.Name)
		}
		if workers.Done() {
			break
		}
	}

	return ticks
}

type Work struct {
	Step  string
	Delay int
}

type Workers struct {
	Count int
	Queue []Work
	Delay int
}

func NewWorkers(count int, delay int) *Workers {
	w := &Workers{Count: count, Delay: delay}
	w.Queue = make([]Work, 0)
	return w
}

func (w *Workers) Tick() []Work {
	new := make([]Work, 0)
	done := make([]Work, 0)
	for _, work := range w.Queue {
		work.Delay -= 1
		if work.Delay == 0 {
			done = append(done, work)
		} else {
			new = append(new, work)
		}
	}
	w.Queue = new
	return done
}

func (w *Workers) AddWork(work Work) bool {
	if len(w.Queue) < w.Count {
		delay := int(work.Step[0]) - 64
		work.Delay = w.Delay + delay
		w.Queue = append(w.Queue, work)
		return true
	}
	return false
}

func (w *Workers) Done() bool {
	return len(w.Queue) == 0
}

func NewSteps() *Steps {
	s := &Steps{}
	s.steps = make(map[string]*Step)
	return s
}

func ReadInput(path string) *Steps {
	f, err := os.Open(path)
	if err != nil {
		panic(fmt.Sprintf("unable to open %s for reading", path))
	}
	defer f.Close()

	steps := NewSteps()

	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		fields := strings.Fields(scanner.Text())
		name := fields[7]
		condition := fields[1]

		_, ok := steps.Get(name)
		if !ok {
			steps.Add(name)
			steps.AddCondition(name, condition)
		} else {
			steps.AddCondition(name, condition)
		}

		_, ok = steps.Get(condition)
		if !ok {
			steps.Add(condition)
		}
	}

	return steps
}

func main() {
	steps := ReadInput(os.Args[1])
	sequence := steps.Solve()
	fmt.Printf("Solution 1: %s\n", sequence)

	steps = ReadInput(os.Args[1])
	ticks := steps.SolveWorkers(5, 60)
	fmt.Printf("Solution 1: %d\n", ticks)
}
