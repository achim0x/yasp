# Software Architecture

The following section describe the high level software architecture

## Use Cases

The following diagram show the main use cases of this application:

```plantuml
@startuml usecases
!theme materia
'possible themes: materia, mars, _none_, reddress-lightblue, spacelab

scale 1.2

left to right direction

title Main use cases

actor User as user

rectangle Application {
  usecase "Update Database" as updateDB
  usecase "Update all elements" as updateAll
  usecase "Update single element" as updateElement
  usecase "Read field configuration" as readFieldConfig
  usecase "Visualistaion of stock information" as visualisation
  usecase "Show all stocks" as showAll
  usecase "Show filtered stocks" as showFiltered
  usecase "Read filter configuration" as readFilter
  usecase "Color Coding" as colorCoding
  usecase "Read Color Codiing filter" as ccFilter
}

user -- updateDB
user -- visualisation


updateAll ..> updateDB : extend
updateElement ..> updateAll : include
updateElement ..> updateDB : include
readFieldConfig ..> updateDB : include
showAll ..> visualisation : extend
showFiltered ..> visualisation : extend
readFilter ..> showFiltered : include
colorCoding ..> showAll : include
ccFilter ..> colorCoding: include
colorCoding ..> showFiltered : include
@enduml
```

## Context Diagram

```plantuml
@startuml
top to bottom direction
skinparam Linetype ortho


package "YASP"{
    [main] as main
    [user_interface] as ui
    [excel_export] as excel
    [db_handler] as db_handler
    [user_def_link] as user_link
}

database filesystem {
file "db_config.json" as db_config
file "api_field_mapping.json" as field_mapping
file "stocks.db (sqlite)" as db
file "stocks.xlsx" as xlsx
}

cloud finance as "financial data provider"
cloud chart as "chart / trading provider"

main .left. ui
main .left.> excel
main .down.> db_handler
 
db_handler <...down.> db       : <<store data>>
db_handler ...down.> db_config : <<read>>
db_handler ...down.> field_mapping: <<read>>
db_handler ...right.> finance  : <<read>>
db_handler ...down.> user_link
user_link ...right.> chart : <<provide reference>>
excel ...down.> xlsx
@enduml
```

## Class Diagram

```plantuml
@startuml classDiagram

package db_handler {
    class DbHandler {
        -dbFile:String
        -apiKey:String
        +__init__()
        +add_isin()
        +get_all(filter)
        +get_watchlist(filter)
        +get_entry(isin, filter)
        +update_all()
        +update_watchlist()
        +update_entry(isin)
        +set_watchlist(isin, state)
    }
}

package yasp_xls {
    class YaspXls{
        +update_all()
        +update_watchlist()
        +update_profiles()
    }
}

package yasp_ui {
    class YaspUi {
        +update_all()
        +update_watchlist()
        +safe_watchlist()
        +show_profiles()
    }
}

package user_def_link {
    class user_def_link <<functions>> {
        +get_chart_link(isin):string
        +get_trading_link(isin):string
    }
}

YaspXls --> DbHandler : uses
YaspUi --> DbHandler : uses
DbHandler --> user_def_link : calls

@enduml
```
