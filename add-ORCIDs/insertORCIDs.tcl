#!/usr/bin/tclsh

set orcidFilename [lindex $argv 0]
set fp [open $orcidFilename r]
set cts [string trim [read $fp]]
close $fp

set authorList ""
foreach line [split $cts "\n"] {
   set items [split $line ";"]
   set orcid [lindex $items 4]
   if {$orcid != ""} {
      if {![regexp "^....\\-....\\-....\\-....$" $orcid]} { 
         puts "INVALID ORCID for: $line"
      }
   }
   set email [lindex $items 3]
   foreach emailitem [split $email ","] {
      set emailitem [string trim $emailitem]
      lappend authorList [list [lindex $items 0] [lindex $items 1] [lindex $items 2] $emailitem $orcid]
   }
}
#puts $authorList
#exit

foreach filename [lrange $argv 1 end] {
   puts "Working on: $filename"
   set fp [open $filename r]
   set cts [string trim [read $fp]]
   close $fp

   set newfilename "xml_with_orcids/[file tail $filename]"
   set fp [open $newfilename w]

   foreach line [split $cts "\n"] {
      if {[regexp "^(\[^<\]*)<surname>(\[^<\]+)</surname>(.*?)$" $line all prefix surname rest]} {
         puts $fp $line
         set currSurname $surname
      } elseif {[regexp "^(\[^<\]*)<forename>(\[^<\]+)</forename>(.*?)$" $line all prefix forename rest]} {
         puts $fp $line
         set currForeame $surname
      } elseif {[regexp "^(\[^<\]*)<email>(\[^<\]+)</email>(.*?)$" $line all prefix email rest]} {
         puts $fp $line
         set idxList [lsearch -all -index 3 $authorList $email]
         if {[llength $idxList] > 0} {
            foreach idx $idxList {
               set orcid [lindex [lindex $authorList $idx] 4] 
               if {$orcid != ""} {
                  break
               }
            }
            if {$orcid != ""} {
               puts "++   AUTHOR $email FOUND, ORCID $orcid ADDED, FILENAME=$filename"
               puts $fp "$prefix<idno type=\"ORCID\">$orcid</idno>" 
            } else {
               puts "+-   AUTHOR $email FOUND, NO ORCID AVAILABLE, FILENAME=$filename"
            }
         } else {
            puts "-?   AUTHOR $email NOT FOUND -> TRYING SURNAME/FORENAME, FILENAME=$filename"
            set idxList [lsearch -all -index 0 $authorList "$surname, $forename"]
            if {[llength $idxList] > 0} {
               foreach idx $idxList {
                  set orcid [lindex [lindex $authorList $idx] 4] 
                  if {$orcid != ""} {
                     break
                  }
               }
               if {$orcid != ""} {
                  puts "++   AUTHOR $surname, $forename FOUND, ORCID $orcid ADDED, FILENAME=$filename"
                  puts $fp "$prefix<idno type=\"ORCID\">$orcid</idno>" 
               } else {
                  puts "+-   AUTHOR $surname, $forename FOUND, NO ORCID AVAILABLE, FILENAME=$filename"
               }
            } else {
               puts "--   AUTHOR $surname, $forename NOT FOUND, FILENAME=$filename"
            }
         }
      } else {
         puts $fp $line
      }
   }

   puts "\n"

   close $fp
}

