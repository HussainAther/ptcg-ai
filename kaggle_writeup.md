# Hybrid Knowledge-Guided Planning for Pokémon TCG AI

## Summary

My proposed agent combines structured game knowledge with search-based planning to make strong, interpretable decisions in Pokémon TCG. Rather than relying on a single machine learning model, the system separates decision making into modular components that can be independently tested and improved.

The current implementation consists of:

* structured card database
* strategic card tagging
* card knowledge graph
* game-state representation
* rule-aware simulation scaffold
* heuristic planner
* one-step lookahead planner
* Monte Carlo Tree Search (MCTS) scaffold
* board evaluation function
* automated regression tests

This modular architecture provides a transparent baseline while allowing progressively stronger planning algorithms to be incorporated over time.

---

# Motivation

Pokémon TCG presents several challenges that distinguish it from perfect-information games.

An effective agent must reason about:

* hidden information
* stochastic card draws
* long-term resource management
* evolving board states
* once-per-turn restrictions
* prize-race optimization
* sequencing decisions
* uncertainty about the opponent's future actions

Because of these characteristics, immediate tactical gains are not always optimal. The strongest decisions often maximize expected future board value rather than immediate damage.

---

# Card Knowledge Layer

The provided English card database contains over 2,000 cards spanning Pokémon, Trainer, Stadium, Tool, and Energy cards.

Instead of treating each card as an isolated object, the system converts every card into structured information including:

* evolution stage
* card type
* HP
* attack information
* rule text
* effect description

From effect text, strategic tags are inferred, including:

* damage pressure
* energy acceleration
* deck search
* draw engine
* bench pressure
* discard synergy
* switching mobility
* healing
* status control
* evolution support
* damage prevention

These tags allow the planner to reason about card functionality instead of memorizing individual card names.

---

# Game State Representation

The simulator represents the complete game using structured player states.

Each player tracks:

* deck
* hand
* discard pile
* prize cards
* active Pokémon
* bench
* once-per-turn Supporter usage
* once-per-turn Energy attachment

Each Pokémon stores:

* HP
* attached Energy
* evolution state
* status conditions
* knockout state

A state encoder converts these symbolic objects into numerical features suitable for planning and future learning algorithms.

---

# Decision Pipeline

The overall decision process follows this sequence:

```
Game State
      ↓
State Encoder
      ↓
Legal Action Generator
      ↓
Board Evaluation
      ↓
Planner
      ↓
Chosen Action
```

Separating these responsibilities keeps the system interpretable while simplifying testing and future development.

---

# Board Evaluation

The board evaluator estimates the quality of a position using several interpretable components.

Current evaluation considers:

* prize race
* active Pokémon HP
* board development
* hand size
* opponent board pressure

Rather than assigning values directly to actions, the planner evaluates the board state that would result after taking an action.

This separation allows different planning algorithms to share the same evaluation function.

---

# Planning Algorithms

Three complementary planning methods are currently supported.

### Heuristic Planner

The heuristic planner scores candidate actions using domain knowledge.

Examples include:

* rewarding immediate knockouts
* prioritizing prize progression
* valuing Energy development
* improving hand consistency
* preserving damaged attackers

This provides a fast and interpretable baseline.

### One-Step Lookahead

The lookahead planner simulates each legal action, evaluates the resulting board, and selects the action producing the strongest position.

This planner already captures tactical situations that simple heuristics may miss.

### Monte Carlo Tree Search

The framework includes a Monte Carlo Tree Search scaffold.

Each search node stores:

* game state
* parent
* children
* visit count
* accumulated value

The search repeatedly performs:

1. selection
2. expansion
3. rollout
4. backpropagation

MCTS naturally balances exploration and exploitation while planning multiple turns into the future.

---

# Engineering Approach

Correctness is emphasized throughout the implementation.

Regression tests currently verify:

* knockout handling
* prize updates
* energy attachment limits
* Supporter restrictions
* retreat behavior
* MCTS decision consistency

During development, testing identified an error in prize accounting inside the simulator. Comparing heuristic and lookahead planners exposed the issue, which was corrected and protected by automated tests. This illustrates the importance of modular design and continuous validation.

---

# Future Improvements

The current implementation establishes the planning architecture rather than a complete simulator.

Future work includes:

* complete implementation of Pokémon TCG rules
* card-specific action generation
* exact attack resolution
* Ability execution
* weakness and resistance
* retreat costs
* stadium interactions
* hidden-information belief modeling
* opponent modeling
* neural value estimation
* self-play reinforcement learning

The modular architecture is designed so these capabilities can be added without restructuring the overall system.

---

# Conclusion

This strategy combines symbolic reasoning with search-based planning to produce an agent that is both interpretable and extensible.

Rather than relying entirely on machine learning or handcrafted heuristics, the framework integrates structured card knowledge, board evaluation, simulation, and Monte Carlo Tree Search into a unified decision pipeline.

This approach provides a strong baseline today while establishing a clear path toward increasingly capable agents through richer simulation, learned value functions, and self-play.

---

## One recommendation before submitting

I would also include **one simple architecture figure** in your repository (or in the Kaggle notebook if the competition allows images). Even a clean diagram like this makes the design much easier to follow:

```text
                     Pokémon TCG AI Framework

                    +----------------------+
                    |   Card Database      |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Knowledge Graph      |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Game State           |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Legal Actions        |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Board Evaluation     |
                    +----------+-----------+
                               |
                 +-------------+-------------+
                 |             |             |
                 v             v             v
          Heuristic      Lookahead        MCTS
                 \             |            /
                  \            |           /
                   +-----------+----------+
                               |
                               v
                      Selected Action
